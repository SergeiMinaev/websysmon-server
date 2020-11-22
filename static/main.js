import {
  get_cookie,
  set_cookie,
  call_api,
  call_remote_api,
  make_el,
} from '/static/utils.js';


const key = get_cookie('key');
const unauth = document.getElementById('unauth');
const unauth__btn = document.getElementById('unauth__btn');
const entities_blank = document.getElementById('entities_blank');
const entity_blank = document.getElementById('entity_blank');
const entity_item_blank = document.getElementById('entity_item_blank');
const entity_items_blank = document.getElementById('entity_items_blank');
const content = document.getElementById('content');

if (!key) {
  unauth.classList.remove('hidden');
  unauth__btn.addEventListener('click', (e) => {
    const key = document.getElementById('unauth__input').value;
    if (key) {
      set_cookie('key', key, 120);
      init();
    }
  });
} else {
  init();
}

async function init() {
  unauth.classList.add('hidden');
  const state = await call_api('state');
  if (state.status == 401) {
    set_cookie('key', false, 0);
    location.reload();
  }

  visualize(state);

  const remote = await call_api('remote');
  const key = get_cookie('key');
  for (let index = 0; index < remote.urls.length; index++) {
    const url = remote.urls[index];
    const state = await call_remote_api(
      `${url}/api/state?key=${key}`);
    visualize(state);
  };
}

function visualize(state) {
  content.classList.remove('hidden');
  const entities_el = entities_blank.cloneNode(true);
  entities_el.appendChild(make_el(
    `<div class="entities__title">${state.server_name}</div>`
  ));
  entities_el.classList.remove('hidden');
  entities_el.removeAttribute('id');
  content.appendChild(entities_el);

  for (const entity in state.entities) {
    const entity_el = entity_blank.cloneNode(true);
    entity_el.classList.remove('hidden');
    entity_el.removeAttribute('id');
    entities_el.appendChild(entity_el);

    const title_el = entity_el.getElementsByClassName('entity__title')[0];
    title_el.innerText = entity;

    const items = entity_items_blank.cloneNode(true);
    items.classList.remove('hidden');
    items.removeAttribute('id');
    const items_title = items.getElementsByClassName('entity__items-title')[0];
    entity_el.appendChild(items);

    items_title.innerText = Object.keys(state.entities[entity])[0];

    for (const svc in state.entities[entity].systemd_services) {
      const entity_item = entity_item_blank.cloneNode(true);
      entity_item.classList.remove('hidden');
      entity_item.removeAttribute('id');
      items.appendChild(entity_item);
      const key = entity_item.getElementsByClassName('entity__item-key')[0];
      const val = entity_item.getElementsByClassName('entity__item-val')[0];
      key.innerText = svc;
      const status_el = make_el('<div class="entity__item-status"></div>');
      if (state.entities[entity].systemd_services[svc].status == 'active') {
        status_el.classList.add('status--ok');
        status_el.innerText = 'ok';
      } else {
        status_el.classList.add('status--er');
        status_el.innerText = 'er';
      }
      val.appendChild(status_el);
    }
  }

  //const globals_el = entities_blank.cloneNode(true);
  //globals_el.classList.remove('hidden');
  //globals_el.removeAttribute('id');
  //content.appendChild(globals_el);
  for (const entity in state.global) {
    const entity_el = entity_blank.cloneNode(true);
    entity_el.classList.remove('hidden');
    entity_el.removeAttribute('id');
    entities_el.appendChild(entity_el);

    const title_el = entity_el.getElementsByClassName('entity__title')[0];
    title_el.innerText = entity;

    const items = entity_items_blank.cloneNode(true);
    items.classList.remove('hidden');
    items.removeAttribute('id');
    entity_el.appendChild(items);

    for (const svc in state.global[entity]) {
      const entity_item = entity_item_blank.cloneNode(true);
      entity_item.classList.remove('hidden');
      entity_item.removeAttribute('id');
      items.appendChild(entity_item);
      const key = entity_item.getElementsByClassName('entity__item-key')[0];
      const val = entity_item.getElementsByClassName('entity__item-val')[0];
      key.innerText = svc;
      const status_el = make_el('<div class="entity__item-status"></div>');
      if (entity == 'partitions') {
        val.innerHTML = `${state.global[entity][svc].avail_perc
          }% space<br>${state.global[entity][svc].iavail_perc}% inodes`;
        if (state.global[entity][svc].avail_perc > 5
          && state.global[entity][svc].iavail_perc > 5) {
          status_el.classList.add('status--ok');
          status_el.innerText = 'ok';
        } else {
          status_el.classList.add('status--er');
          status_el.innerText = 'er';
        }

      } else if (entity == 'urls') {
        if (state.global[entity][svc].status_code == 200) {
          status_el.classList.add('status--ok');
          status_el.innerText = 'ok';
        } else {
          status_el.classList.add('status--er');
          status_el.innerText = 'er';
        }
      }
      val.appendChild(status_el);
    }
  }
}
