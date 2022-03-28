"user strict";
// Блок для инициализации редактора текста tinymce
tinyMCE.init({
    selector: '#id_task_text',

    height: "400",
    toolbar: 'undo redo | styleselect | codesample | code',
    style_formats: [{
        title: 'text',
        block: 'p'
    }, {
        title: 'header h4',
        block: 'h4'
    }, {
        title: 'header h5',
        block: 'h5'
    },],
    menubar: false,
    plugins: ['codesample code', 'paste'],
    paste_block_drop: false,
    paste_as_text: true,
    init_instance_callback: 'onTinyLoad',
    codesample_languages: [
        { text: 'Python', value: 'python' },
        { text: 'Java', value: 'java' },
        { text: 'C', value: 'c' },
        { text: 'C#', value: 'csharp' },
        { text: 'C++', value: 'cpp' }
    ],
});

// Блок для копирования содержимого tinymce при submit в скрытый блок ввода для отправки на сервер
let submit = document.querySelector('#submit');

submit.addEventListener('click', function (event) {
    let data = tinymce.get('id_task_text').getContent();
    let task_text_tag = document.querySelector('#id_task_text');
    task_text_tag.innerHTML = data;
});

// Блок для изменения окна редактора tiny

function onTinyLoad() {

    let div = document.createElement('div');
    div.classList.add('tox-toolbar__group');
    div.classList.add('ms-2');
    div.textContent = "enter - новый абзац; shift+enter - перенос строки";
    document.querySelector('.tox-toolbar__primary').append(div);
}


//////////////////////////////////////////////////////////////////
// Вытащить теги при submit в скрытом блоке множественного выбора тегов, 
// для отправки на сервер. Сервер воспринимает именно это поле.
class ElementNotExistInBDError extends Error {
    constructor(message) {
        super(message); // (1)
        this.name = "ValidationError"; // (2)
    }
}

class DuplicationSlugError extends Error {
    constructor(message, elemName = Null, errorFromServer = Null) {
        super(message);
        this.name = "ValidationError";
        this.elemName = elemName;
        this.errorFromServer = errorFromServer;
    }
}


class Tags {

    constructor() {
        let tagWrapper = document.querySelector('.tag-wrapper');
        let plus = tagWrapper.querySelector('img');
        plus.addEventListener('click',
            (event) => tags.addInput(event, tagWrapper, plus));
    }

    submitTags(event) {
        this.inputs = document.querySelectorAll('.input_tag_real');
        this.multi = document.getElementById('id_tag');
        this.resetMulti(this.multi);
        this.inputsToMulti(this.inputs, this.multi, event);
        event.preventDefault();
    }

    resetMulti(multi) {
        let options = multi.querySelectorAll('option');
        for (let option of options) {
            option.selected = false;
        }
    }

    inputsToMulti(inputs, multi, event = null) {
        for (let input of inputs) {
            if (!input.value) continue;
            try {
                this.inputToMulti(input, multi);
            } catch (err) {
                if (err instanceof ElementNotExistInBDError) {
                    let needTag = confirm(`Выбранный вами тег ${input.value} не существует. Создать?`);
                    if (needTag) {
                        // Необходимо добавить тег в БД
                        let dataPromis = this.addTagToBD(input.value);
                        dataPromis.then(data => {
                            // Обновить multi                     

                            let dataJson = JSON.parse(data['tags']);

                            let tagsName = Object.entries(dataJson).map(entry => {
                                return entry[1]['fields']['name'];
                            });
                            let tagsPK = Object.entries(dataJson).map(entry => {
                                return entry[1]['pk'];
                            });

                            this.updateMulti(tagsName, tagsPK, multi);
                            // Пробуем снова сделать sumbit
                            setTimeout(() => this.submitTags.bind(this)(event), 100)
                        })
                            .catch((err) => {
                                let errorTag = document.getElementById('tag-error');
                                console.log(err);
                                let message = `Повтор slug для тега ${err.tagName}. Просьба поменять название тега.`;
                                this.printError(errorTag, message);
                            });
                        return;

                    } else {
                        if (event) {
                            event.preventDefault();
                        }
                        return;
                    }
                } else {
                    throw err;
                }
            }
        }
        setTimeout(() => {
            let form = document.querySelector('#create-exercise');
            HTMLFormElement.prototype.submit.call(form);
        }, 100);
    }



    updateMulti(tagsName, tagsPK, multi) {
        // console.log(tagsName);
        // console.log(tagsPK);

        let options = multi.querySelectorAll('option');
        Array.from(options).forEach(item => item.remove());
        for (let num = 0; num < tagsName.length; num++) {
            let tagName = tagsName[num];
            let tagPK = tagsPK[num];
            let optionTemplate = options[0].cloneNode(false);
            optionTemplate.value = tagPK;
            optionTemplate.textContent = tagName;
            let newOption = optionTemplate;
            multi.append(newOption);
        }
    }

    printError(errorTag, error) {
        errorTag.textContent = error;
        errorTag.hidden = false;
    }

    addTagToBD(nameTag) {
        const data = {
            'name': nameTag,
        };
        function getCookie(name) {
            var cookieValue = null;
            if (document.cookie && document.cookie !== '') {
                var cookies = document.cookie.split(';');
                for (var i = 0; i < cookies.length; i++) {
                    var cookie = cookies[i].trim();
                    // Does this cookie string begin with the name we want?
                    if (cookie.substring(0, name.length + 1) === (name + '=')) {
                        cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                        break;
                    }
                }
            }
            return cookieValue;
        }
        let csrftoken = getCookie('csrftoken');

        const init = {
            method: 'POST',
            mode: 'cors',
            cache: 'no-cache',
            credentials: 'include',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken,
            },
            redirect: 'follow',
            referrerPolicy: 'no-referrer',
            body: JSON.stringify(data)
        };

        const relativeTagUrl = labelTags.dataset.createTagUrl;
        const protocol = window.location.protocol;
        let baseUrl = protocol + '//' + window.location.host

        const url = new URL(relativeTagUrl, baseUrl);
        let responseData = null;
        ///////////////////////////////////////////////////////////////
        let promis = fetch(url, init)
            .then(response => {
                return response.json();
            })
            .then(data => {
                if (data.error === 'Null') {
                    return data;
                } else {
                    // Выдать ошибку в код html
                    let arr = DuplicationSlugError('Повтор тега', nameTag, data.error);
                    throw arr;
                }
            }).catch(error => alert(error));
        return promis;
    }

    inputToMulti(input, multi) {
        let options = multi.querySelectorAll('option');
        let isFindTag = false;
        let selected = [];
        for (let option of options) {
            if (input.value === option.textContent) {
                selected.push(Number(option.value));
                option.selected = true;
                isFindTag = true;
                break;
            }
        }

        if (!isFindTag) {
            throw new ElementNotExistInBDError("Данного тега нет в базе данных");
        }
    }

    addInput(event, tagWrapper, plus) {
        // Сделать копию блока с тегом и вставить ее вниз
        let anotherTagWrapper = tagWrapper.cloneNode(true);
        anotherTagWrapper.querySelector('input').value = '';
        tagWrapper.after(anotherTagWrapper);
        plus.remove();
        let anotherPlus = anotherTagWrapper.querySelector('img');
        anotherPlus.addEventListener('click',
            (event) => {
                tags.addInput(event, anotherTagWrapper, anotherPlus)
            });
    }

    multiToInput() {
        // Прочитать все выделение из мульти

        let multi = document.getElementById('id_tag');

        let options = multi.querySelectorAll('option');
        let selected = [];
        for (let option of options) {
            if (option.selected) {
                selected.push(option.textContent);
            }
        }

        let anotherTagWrapper = null;
        let anotherPlus = null;
        let tagWrapper = document.querySelector('.tag-wrapper');
        let input = null;
        let plus = null;
        // Создать нужное количество input
        for (let select of selected) {
            input = tagWrapper.querySelector('input');
            plus = tagWrapper.querySelector('img');
            console.log(select);
            input.value = select;

            anotherTagWrapper = tagWrapper.cloneNode(true);
            tagWrapper.after(anotherTagWrapper);
            tagWrapper = anotherTagWrapper;
            plus.remove();
            input = tagWrapper.querySelector('input');
            input.value = '';
        }

        if (selected.length) {
            plus = tagWrapper.querySelector('img');
            plus.addEventListener('click',
                (event) => {
                    tags.addInput(event, tagWrapper, plus)
                });
        }


    }
}

let tags = new Tags();

// Подтянем значение из multi. Применяется для редактирования задачи.
tags.multiToInput();

submit.addEventListener('click', event => tags.submitTags(event));

//////////////////////////////////////////////////////////////////
