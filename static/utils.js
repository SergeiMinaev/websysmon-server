export const get_cookie = (name) => {
  let a = `; ${document.cookie}`.match(`;\\s*${name}=([^;]+)`);
  return a ? a[1] : '';
}
export function set_cookie(name,value,days) {
    var expires = "";
    if (days) {
        var date = new Date();
        date.setTime(date.getTime() + (days*24*60*60*1000));
        expires = "; expires=" + date.toUTCString();
    }
    document.cookie = name + "=" + (value || "")  + expires + "; path=/";
}

export async function call_api(method) {
  const resp = await fetch(`/api/${method}`)
    .then(function(response) {
      if (response.status === 200) {
        return response.json();
      } else {
        return response;
      }
    })
    .catch(function(err) {
      console.error(err);
    });

  return resp;
}

export async function call_remote_api(url) {
  const resp = await fetch(url)
    .then(function(response) {
      if (response.status === 200) {
        return response.json();
      } else {
        return response;
      }
    })
    .catch(function(err) {
      console.error(err);
    });

  return resp;
}

export function make_el(html) {
  let temp = document.createElement('template');
  html = html.trim();
  temp.innerHTML = html;
  return temp.content.firstChild;
}
