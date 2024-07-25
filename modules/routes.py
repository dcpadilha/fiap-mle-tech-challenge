from http import HTTPStatus

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm

from modules.export import download_file
from modules.file_utils import read_file

# User Modules
from modules.schemas import DownloadList
from modules.scraping import scrape_url
from modules.security import (
    create_access_token,
    get_current_user,
    get_password_hash,
    verify_password,
)
from modules.user_exceptions import FileHandlingError

router = APIRouter()

# Endpoint for the Load Balancer Health Check
@router.get('/mlet/ping', status_code=HTTPStatus.OK)
def ping():
    # Return value doesn't matter, as long as the HTTP Status is 200
    return "OK"

# Endpoint to scrape available download links
@router.get('/list_links', status_code=HTTPStatus.OK)
def list_links(request: Request, current_user=Depends(get_current_user)):
    if not current_user['user']:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Unauthorized')

    links = request.app.database['scrape_target'].find_one()

    links.pop('_id')

    return scrape_url(links)


@router.post('/export_file', status_code=HTTPStatus.OK)
async def export_file(download_list: DownloadList, request: Request, current_user=Depends(get_current_user)):
    if not current_user['user']:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Unauthorized')

    files_downloaded = []

    for link in download_list.available_downloads:
        # Downloads the file and returns the generated filename
        downloaded_file = download_file(link)

        # Raises an exception in case the file could not be downloaded
        if not downloaded_file:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Download error, verify the link')

        files_downloaded.append(downloaded_file)

    # if(save_to_db):
    #     request.app.database['exported_data'].save( { downloaded_file : show_file(download_file) })

    # return download_list
    return {'files': files_downloaded}


@router.get('/show_file/{filename}', status_code=HTTPStatus.OK)
def show_file(filename: str, current_user=Depends(get_current_user)):
    """
    Reads the contents of a file already downloaded
    """

    if not current_user['user']:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Unauthorized')

    try:
        file_contents = read_file(filename)
    except FileHandlingError as e:
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail=e.message)

    return file_contents


@router.post('/encrypt_pwd')
def encrypt_pwd(credential=Body(...)):
    plain_password = credential['password']
    return {'encrypted_password': get_password_hash(plain_password)}


@router.post('/token')
def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    query = {'user': form_data.username}
    user = request.app.database['users'].find_one(query)

    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    if not verify_password(form_data.password, user['password']):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': form_data.username})

    return {'access_token': access_token, 'token_type': 'bearer'}
