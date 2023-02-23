from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm.session import Session
from src.auth.authentication_api import get_db
from src.models.media_file import medi_model as model
from src.models.media_file.medi_model import Media
from src.models.media_file.media_schema import MediaSchema

router_media = APIRouter(prefix='/media')

@router_media.get("/{media_id}/")
def get_mediafile(media_id: int, db: Session = Depends(get_db)):
    mediafile = db.query(Media).filter(Media.id == media_id).first()

    if not mediafile:
        raise HTTPException(status_code=404, detail="Mediafile doesn't exist")

    return mediafile

#
@router_media.post("/add-mediafile/")
def add_mediafile(new_mediafile: MediaSchema, db: Session = Depends(get_db)):
    create_mediafile_model = model.Media()
    create_mediafile_model.name = new_mediafile.name
    create_mediafile_model.link = new_mediafile.link

    try:
        db.add(create_mediafile_model)
        db.commit()

    except IntegrityError:
        raise HTTPException(status_code=400, detail="Mediafile already exists")

    return "MediaFile has been added"
#
#
@router_media.patch("/update-mediafile/{media_id}")
def update_media(media_id: int, media: MediaSchema, db: Session = Depends(get_db)):
    update_mediafile = db.query(Media).filter(Media.id == media_id).first()

    if not update_mediafile:
        raise HTTPException(status_code=400, detail="Mediafile doesn't exist")

    update_mediafile.name = media.name
    update_mediafile.link = media.link

    db.commit()

    return "Mediafile has been updated"


@router_media.delete("/delete-mediafile/{media_id}")
def delete_mediafile(media_id: int, db: Session = Depends(get_db)):

    media = db.query(Media).filter(Media.id == media_id).first()

    if not media:
        raise HTTPException(status_code=404, detail="Mediafile doesn't exist")

    db.delete(media)
    db.commit()

    return "Mediafile has been deleted"