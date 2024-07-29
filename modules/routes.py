from http import HTTPStatus
import os

from fastapi import APIRouter, Body, Depends, HTTPException, Request
from fastapi.security import OAuth2PasswordRequestForm

from modules.file_utils import download_file, read_file

# User Modules
from modules.schemas import DownloadList, UserInfo
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
@router.get('/ping', status_code=HTTPStatus.OK)
def ping():
    """
    Dummy endpoint to return HTTP Status 200.
    Return value doesn't matter, as long as the HTTP Status is 200.
    This endpoint is used by the ECS service to validate that the container is successfully deployed.

    Parameters
    ----------
    No parameters required to call this endpoint.

    Returns
    -------
    str
        This endpoint will return the string "OK".

    Examples
    --------
    Nothing to be presented as example. This is a simple GET call.
    """
    return 'OK'


@router.get('/list_links', status_code=HTTPStatus.OK)
def list_links(request: Request, current_user=Depends(get_current_user)):
    """
    Endpoint to scrape available download links

    Parameters
    ----------
    request : Request
        The Request object used to access the database.
    current_user : dict
        Injected by the get_current_user dependency.

    Returns
    -------
    dict
        A dictionary containing a list of available download links.

    Examples
    --------
    A simple GET call on this endpoint should return an output similar to the below:

    {
        "available_downloads": [
            "http://vitibrasil.cnpuv.embrapa.br/download/Producao.csv",
            ... output ommitted 
            "http://vitibrasil.cnpuv.embrapa.br/download/ExpSuco.csv"
        ]
    }
    """
    if not current_user['user']:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Unauthorized')

    # links = get_scrape_links(request)
    links = request.app.database.get_scrape_links()
    print(f'Links to be scraped: {links}')

    # links.pop('_id')

    return scrape_url(links)


@router.post('/export_file', status_code=HTTPStatus.OK)
async def export_file(download_list: DownloadList, request: Request, current_user=Depends(get_current_user)):
    if not current_user['user']:
        raise HTTPException(status_code=HTTPStatus.UNAUTHORIZED, detail='Unauthorized')

    files_downloaded = []

    # Goes through a list of URLs with the download links
    for link in download_list.available_downloads:
        # Downloads the file and returns the generated filename
        downloaded_file = download_file(link)

        # Raises an exception in case the file could not be downloaded
        if not downloaded_file:
            raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail='Download error, verify the link')

        # Appends the generated file name to the list which will be returned by the API
        files_downloaded.append(downloaded_file)

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


@router.post('/add_user')
def add_user(request: Request, user_info: UserInfo):
    user_info.password = get_password_hash(user_info.password)

    try:
        request.app.database.add_user(user_info)
        return {'message': 'User successfully added'}
    except Exception as e:
        raise HTTPException(status_code=HTTPStatus.NOT_MODIFIED, detail=e.message)


@router.post('/encrypt_pwd')
def encrypt_pwd(credential=Body(...)):
    plain_password = credential['password']
    return {'encrypted_password': get_password_hash(plain_password)}


@router.post('/token')
def login_for_access_token(
    request: Request,
    form_data: OAuth2PasswordRequestForm = Depends(),
):
    # user = get_user_info(request, form_data)
    query = {'user': form_data.username}
    print(f'Query: {query}')
    user = request.app.database.get_user_info(query)

    print(f'Returned User: {user}')

    if user is None:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    if not verify_password(form_data.password, user['password']):
        print(f'Triggering error')
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail='Incorrect email or password',
        )

    access_token = create_access_token(data={'sub': form_data.username})

    return {'access_token': access_token, 'token_type': 'bearer'}
