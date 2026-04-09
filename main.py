from budget import create_app



app = create_app()  # create_app is defined in __init__.py



if __name__ == '__main__':
    app.run(debug=True)