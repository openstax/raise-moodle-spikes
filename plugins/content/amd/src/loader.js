import Event from 'core/event';

export const load = () => {
  const osx_content_items = document.querySelectorAll('.osx-raise-content');

  osx_content_items.forEach(async (elem) => {
    const request = new Request(`http://localhost:8800/contents/${elem.dataset.id}`);
    const response = await fetch(request);
    const data = await response.json();

    elem.innerHTML = `<div class="filter_mathjaxloader_equation">${data.content}</div>`;
    Event.notifyFilterContentUpdated(elem);
  });
};
