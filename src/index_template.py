from flask import render_template_string

def template(app):
    with app.app_context():
        return render_template_string('''
        <!doctype html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport"
                  content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
            <meta http-equiv="X-UA-Compatible" content="ie=edge">
            <meta name="description" content="Simple file drop server.">
                <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@picocss/pico@1/css/pico.min.css" />
            <title>Filedrop</title>
            <style>
                #drop_zone {
                    border: 3px dashed gray;
                    width: 100%;
                    height: 200px;
                }

                .drop-zone-text {
                    text-align: center;
                    position: relative;
                    top: 50%;
                    transform: translateY(-50%);
                }

                .center {
                    text-align: center;
                }
            </style>
        </head>
        <body>
        <main class="container">
            <article>
                <div class="container">
                    <div id="drop_zone" ondrop="dropHandler(event);" ondragover="dragOverHandler(event);"
                         onclick="openFileSelector();">
                        <p class="drop-zone-text">Drag files here</p>
                    </div>
                    <input type="file" id="file_selector" name="files" accept="image/*" multiple required>
                </div>
                <br>
                <progress hidden id="progress" value="25" max="100"></progress>
                <br>
                <button onclick="uploadFiles()">Upload</button>
            </article>
        </main>
        </body>

        <script>
            function dropHandler(ev) {
                console.log('File(s) dropped');
                ev.preventDefault();

                if (ev.dataTransfer.items) {
                    [...ev.dataTransfer.items].forEach((item, i) => {
                        if (item.kind === 'file') {
                            const file = item.getAsFile();
                            console.log(`… file[${i}].name = ${file.name}`);
                        }
                    });
                } else {
                    [...ev.dataTransfer.files].forEach((file, i) => {
                        console.log(`… file[${i}].name = ${file.name}`);
                    });
                }

                // add files to file_selector
                document.getElementById('file_selector').files = ev.dataTransfer.files;
            }

            function dragOverHandler(ev) {
                ev.preventDefault();
            }

            function openFileSelector() {
                document.getElementById('file-selector').click();
            }

            function uploadFiles() {
                // abort if files is empty
                if (document.getElementById('file_selector').files.length === 0) {
                    return;
                }

                // upload files from "file_selector" to "/upload" via post
                // show progress in the porogress bar

                // make formDate object
                const formData = new FormData();
                [...document.getElementById('file_selector').files].forEach((file, i) => {
                    console.log(file)
                    formData.append(`file${i}`, file);
                });

                // make request
                const xhr = new XMLHttpRequest();
                xhr.open('POST', '/upload');
                // show progressbar
                document.querySelector('#progress').hidden = false;
                xhr.upload.onprogress = function (e) {
                    if (e.lengthComputable) {
                        const percentComplete = (e.loaded / e.total) * 100;
                        console.log(percentComplete);
                        document.querySelector('#progress').value = percentComplete;
                    }
                };

                xhr.onload = function () {
                    if (this.status === 200) {
                        console.log('Upload complete');
                        const buttonColor = document.querySelector('button').style.backgroundColor;
                        document.querySelector('button').style.backgroundColor = 'green';
                        document.querySelector('button').innerText = 'Uploaded!';
                        setTimeout(() => {
                            document.querySelector('button').style.backgroundColor = buttonColor;
                            document.querySelector('button').innerText = 'Upload';
                        }, 3000);
                    } else {
                        console.error('Upload failed');
                    }

                    // hide and reset progressbar
                    document.querySelector('#progress').hidden = true;
                    document.querySelector('#progress').value = 0;

                    // reset file_selector
                    document.getElementById('file_selector').value = '';
                };

                console.log(formData);
                xhr.send(formData);
            }
        </script>

        </html>
        ''')
