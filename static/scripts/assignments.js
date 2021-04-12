let assignments = {}

function sleep(ms) {
  return new Promise(resolve => setTimeout(resolve, ms));
}

function cmpJQuery(sel1, sel2) {
    let response = true
    if (sel1.length === sel2.length) {
        for (let i = 0; i < sel1.length; i++) {
            if (!(sel1[i] === sel2[i])) {
                response = false
            }
        }
    } else {
        response = false
    }

    return response

}

function updateTitle() {
    for (const i in assignments) {
        if (cmpJQuery(assignments[i].items, assignments[i].items.filter('[style*="none"]'))) {
            assignments[i].title.hide()
        } else {
            assignments[i].title.show()
        }
        if (cmpJQuery(assignments[i].items, assignments[i].items.filter('[style*="opacity: 0;"]'))) {
            assignments[i].title.css('opacity', '0');
        } else {
            assignments[i].title.css('opacity', '100');
        }
    }
}

function store(id, action) {
    let item = window.localStorage.getItem('finished');
    let values = (item ? item.split(',') : [])
    switch (action) {
        case 'add':
            values.push(id);
            break;
        case 'remove':
            values = values.filter(item => item !== id.toString());
            break;
        case 'check':
            return (id.toString() in values);
        case 'list':
            return values;
    }
    window.localStorage.setItem('finished', values);
}

async function hide(transition = false) {
    let list = store(1, 'list');
    for (const i in list) {
        let item = list[i];
        console.log(item);
        let card = $('#' + item);
        card.css('opacity', '0');

    }
    updateTitle()
    await sleep(1000);

    for (const i in list) {
        let item = list[i];
        console.log(item);
        let card = $('#' + item);
        card.hide();

        let button = $('#' + item + ' button')[0];
        button.innerText = 'Undo'
        button.attributes.onclick.value = 'undo(' + item + ');'
    }
    updateTitle()
}

function show() {
    $('.card').hide();
    let list = store(1, 'list');
    for (const i in list) {
        let item = list[i];
        console.log(item);
        $('#' + item).show();
    }
    for (const i in list) {
        let item = list[i];
        console.log(item);
        $('#' + item).css('opacity', '100');
    }
    updateTitle()
    let button = $('.main button:last')[0];
    button.innerText = 'Back'
    button.attributes.onclick.value = 'location.reload();'
}

function undo(id) {
    store(id, 'remove');
    show();
}

function done(id) {
    const audio = new Audio('/static/other/complete.mp3');
    audio.play();
    store(id, 'add');
    hide();
}

$(document).ready(function () {
    let dates = new Set;
    $('.card-subtitle').each(function() {
        dates.add(
            $(this).text().trim()
        )
    });
    console.log(dates)



    dates.forEach(function (item) {
        $('.main').prepend($('<h4 class="work-title">' + item + ': </h4>'))
        assignments[item] = {
            items: $(`.card:contains("${item}")`),
            title: $(`.work-title:contains("${item}")`),
        }
        assignments[item].items.insertAfter(assignments[item].title)
    })

    console.log(assignments)


    let list = store(1, 'list');
    list.forEach(item => {
        console.log(item);
        $('#' + item).hide();

        let button = $('#' + item + ' button')[0];
        button.innerText = 'Undo'
        button.attributes.onclick.value = 'undo(' + item + ');'
    });
    updateTitle()
});