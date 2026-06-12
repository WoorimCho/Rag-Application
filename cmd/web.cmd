@echo off

if (%FLASK_RUN_PORT%)==() set FLASK_RUN_PORT=60010

if (%1)==() goto Usage
if (%1)==(embed) goto fun_embed %2
if (%1)==(list) goto fun_list
if (%1)==(delete) goto fun_delete %2
if (%1)==(query) goto fun_query %2


:Usage
echo. FLASK_RUN_PORT=[%FLASK_RUN_PORT%]
echo.    for updating the port, use the command: set FLASK_RUN_PORT=60010
echo.
echo. Usage: web.cmd [embed^|query] [arguments]
echo.               embed [filename]       : Embeds documents into the vector database.
echo.               list                   : Lists all documents in the vector database.
echo.               delete [document_id]   : Deletes a document from the vector database by its ID.
echo.               query [query text]     : Queries the vector database with a given query.
echo.
goto :eof

:fun_embed
echo Embedding documents...
echo.     curl --request POST --url http://192.168.1.41:%FLASK_RUN_PORT%/embed --header 'Content-Type: multipart/form-data' --form file=@%2
call curl --request POST --url http://192.168.1.41:%FLASK_RUN_PORT%/embed --header 'Content-Type: multipart/form-data' --form file=@%2

echo Embedding completed.
goto :eof

:fun_list
echo Listing documents in the vector database...
echo.    curl --request GET --url http://192.168.1.41:%FLASK_RUN_PORT%/list
::curl --request GET --url http://192.168.1.41:%FLASK_RUN_PORT%/list
curl --request GET --url http://192.168.1.41:%FLASK_RUN_PORT%/list | powershell -Command "($input | ConvertFrom-Json) | ForEach-Object { Write-Host ('ID: ' + $_.id + ' | File: ' + $_.metadatas.source) }"
echo List completed.
goto :eof

:fun_delete
if (%2)==() (
    echo Please provide a document ID to delete.
    goto :eof
)
echo Deleting document with ID %2...
echo.    curl --request DELETE --url http://192.168.1.41:%FLASK_RUN_PORT%/delete/%2
curl --request DELETE --url http://192.168.1.41:%FLASK_RUN_PORT%/delete/%2
echo Deletion completed.
goto :eof

:fun_query
echo Querying the vector database...
echo.    curl --request POST --url http://192.168.1.41:%FLASK_RUN_PORT%/query --header "Content-Type: application/json" --data "{ \"query\": \"%*\" }"
curl --request POST --url http://192.168.1.41:%FLASK_RUN_PORT%/query --header "Content-Type: application/json" --data "{ \"query\": \"%*\" }"
echo Query completed.
goto :eof
