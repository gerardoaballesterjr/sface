import cv2, numpy, onnxruntime

class Detector(object):
    def __init__(self):
        self.model = onnxruntime.InferenceSession('core/seminar/models/face.onnx')
        self.color = (0, 255, 0)

    def area_of(self, left_top, right_bottom):
        hw = numpy.clip(right_bottom - left_top, 0.0, None)
        return hw[..., 0] * hw[..., 1]

    def iou_of(self, boxes0, boxes1, eps=1e-5):
        overlap_left_top = numpy.maximum(boxes0[..., :2], boxes1[..., :2])
        overlap_right_bottom = numpy.minimum(boxes0[..., 2:], boxes1[..., 2:])
        overlap_area = self.area_of(overlap_left_top, overlap_right_bottom)
        area0 = self.area_of(boxes0[..., :2], boxes0[..., 2:])
        area1 = self.area_of(boxes1[..., :2], boxes1[..., 2:])
        return overlap_area / (area0 + area1 - overlap_area + eps)

    def hard_nms(self, box_scores, iou_threshold, top_k=-1, candidate_size=100):
        scores = box_scores[:, -1]
        boxes = box_scores[:, :-1]
        picked = []
        indexes = numpy.argsort(scores)
        indexes = indexes[-candidate_size:]
        while len(indexes) > 0:
            current = indexes[-1]
            picked.append(current)
            if 0 < top_k == len(picked) or len(indexes) == 1:
                break
            current_box = boxes[current, :]
            indexes = indexes[:-1]
            rest_boxes = boxes[indexes, :]
            iou = self.iou_of(rest_boxes, numpy.expand_dims(current_box, axis=0),)
            indexes = indexes[iou <= iou_threshold]
        return box_scores[picked, :]

    def predict(self, width, height, confidences, boxes, prob_threshold, iou_threshold=0.5, top_k=-1):
        boxes = boxes[0]
        confidences = confidences[0]
        picked_box_probs = []
        picked_labels = []
        for class_index in range(1, confidences.shape[1]):
            probs = confidences[:, class_index]
            mask = probs > prob_threshold
            probs = probs[mask]
            if probs.shape[0] == 0:
                continue
            subset_boxes = boxes[mask, :]
            box_probs = numpy.concatenate([subset_boxes, probs.reshape(-1, 1)], axis=1)
            box_probs = self.hard_nms(box_probs,iou_threshold=iou_threshold, top_k=top_k,)
            picked_box_probs.append(box_probs)
            picked_labels.extend([class_index] * box_probs.shape[0])
        if not picked_box_probs:
            return numpy.array([]), numpy.array([]), numpy.array([])
        picked_box_probs = numpy.concatenate(picked_box_probs)
        picked_box_probs[:, 0] *= width
        picked_box_probs[:, 1] *= height
        picked_box_probs[:, 2] *= width
        picked_box_probs[:, 3] *= height
        return picked_box_probs[:, :4].astype(numpy.int32), numpy.array(picked_labels), picked_box_probs[:, 4]

    def scale(self, box):
        width = box[2] - box[0]
        height = box[3] - box[1]
        maximum = max(width, height)
        dx = int((maximum - width)/2)
        dy = int((maximum - height)/2)
        bboxes = [box[0] - dx, box[1] - dy, box[2] + dx, box[3] + dy]
        return bboxes

    def crop(self, frame, box, image_size):
        try:
            face = frame[box[1]:box[3], box[0]:box[2]]
            face = cv2.cvtColor(face, cv2.COLOR_BGR2GRAY)
            return cv2.resize(face, (image_size, image_size), interpolation=cv2.INTER_AREA)
        except:
            return None
        
    def process(self, orig_image, threshold = 0.7):
        image = cv2.cvtColor(orig_image, cv2.COLOR_BGR2RGB)
        image = cv2.resize(image, (320, 240))
        image_mean = numpy.array([127, 127, 127])
        image = (image - image_mean) / 128
        image = numpy.transpose(image, [2, 0, 1])
        image = numpy.expand_dims(image, axis=0)
        image = image.astype(numpy.float32)
        confidences, boxes = self.model.run(None, {self.model.get_inputs()[0].name: image})
        boxes, labels, probs = self.predict(orig_image.shape[1], orig_image.shape[0], confidences, boxes, threshold)
        return boxes, labels, probs

    def draw_border(self, img, pt1, pt2, color, thickness, r, d):
        x1, y1 = pt1
        x2, y2 = pt2
        cv2.line(img, (x1 + r, y1), (x1 + r + d, y1), color, thickness)
        cv2.line(img, (x1, y1 + r), (x1, y1 + r + d), color, thickness)
        cv2.ellipse(img, (x1 + r, y1 + r), (r, r), 180, 0, 90, color, thickness)
        cv2.line(img, (x2 - r, y1), (x2 - r - d, y1), color, thickness)
        cv2.line(img, (x2, y1 + r), (x2, y1 + r + d), color, thickness)
        cv2.ellipse(img, (x2 - r, y1 + r), (r, r), 270, 0, 90, color, thickness)
        cv2.line(img, (x1 + r, y2), (x1 + r + d, y2), color, thickness)
        cv2.line(img, (x1, y2 - r), (x1, y2 - r - d), color, thickness)
        cv2.ellipse(img, (x1 + r, y2 - r), (r, r), 90, 0, 90, color, thickness)
        cv2.line(img, (x2 - r, y2), (x2 - r - d, y2), color, thickness)
        cv2.line(img, (x2, y2 - r), (x2, y2 - r - d), color, thickness)
        cv2.ellipse(img, (x2 - r, y2 - r), (r, r), 0, 0, 90, color, thickness)

    def extract(self, frame, image_size=48):
        boxes_, _, _ = self.process(frame)
        faces, boxes = [], []
        for index in range(boxes_.shape[0]):
            box = self.scale(boxes_[index, :])
            face = self.crop(frame, box, image_size)
            if face is not None:
                faces.append(face)
                boxes.append(box)
            self.draw_border(frame, (box[0], box[1]), (box[2], box[3]), self.color, 1, 3, 8)
        faces = numpy.array(faces).reshape(-1, image_size, image_size, 1).astype(numpy.float32) / 255.0 if faces else faces
        return faces, boxes

class Predictor(object):
    def __init__(self):
        self.model = onnxruntime.InferenceSession('core/seminar/models/model.onnx')
        self.detector = Detector()

    def predict(self, faces):
        try:
            return self.model.run(None, {self.model.get_inputs()[0].name: faces})[0]
        except Exception as exception:
            raise Exception(exception)

    def put_text(self, frame, label, box, x, y):
        font_scale = min(box[2]-box[0], box[3]-box[1])/200
        x = int(x * font_scale)
        y = int(y * font_scale)
        cv2.putText(frame, str(label).upper(), (box[0]+x, box[1]+y), cv2.FONT_HERSHEY_PLAIN, font_scale, self.detector.color, 1)

    def extract(self, predictions, frame, box, x, y, labels):
        label = labels[numpy.argmax(predictions)]
        self.put_text(frame, label, box, x, y)

    def process(self, frame):
        faces, boxes = self.detector.extract(frame)
        if boxes:
            results = self.predict(faces)
            for index, predictions in enumerate(results):
                self.extract(predictions[:7], frame, boxes[index], 10, 25, ['0-2', '10-20', '21-27', '28-45', '3-9', '46-65', '66-116'])
                self.extract(predictions[7:9], frame, boxes[index], 10, 40, ['female', 'male'])
                self.extract(predictions[9:], frame, boxes[index], 10, 55, ['angry', 'fear', 'happy', 'neutral', 'sad', 'surprise'])
            return results
        return None

predictor = Predictor()