import uvicorn
from fastapi import FastAPI
from controllers import upload_csv_controller, list_files_controller, get_file_controller,publisher_controller
from configuration.loggerconf import configure_logger



app = FastAPI()

app.include_router(upload_csv_controller.router)
app.include_router(list_files_controller.router)
app.include_router(get_file_controller.router)
app.include_router(publisher_controller.router)


if __name__ == "__main__":
    configure_logger()

    uvicorn.run(app, host="localhost", port=8080)
