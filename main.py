from website import create_app

app = create_app()

# only if we run this file directly, not if we import this file, we'll execut the following line
if __name__ == '__main__': 
    # 'True' allows to automatically rerun the server after every update
    # turn to "False" when finsih
    app.run(debug=True)
