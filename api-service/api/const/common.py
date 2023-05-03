from fastapi_utils.enums import StrEnum


class AnnotationJobType(StrEnum):
    gallery_images = "gallery_images"
    user_images = "user_images"


class AnnotationTaskType(StrEnum):
    gallery_images = "gallery_images"
    user_images = "user_images"


class AnnotationJobState(StrEnum):
    draft = "draft"
    done = "done"
    error = "error"
    deleted = "deleted"


class AnnotationTaskState(StrEnum):
    draft = "draft"
    skip = "skipped"
    annotated = "annotated"
    merged = "merged"
    done = "done"
    ready = "ready"
    error = "error"
    deleted = "deleted"
