var td = document.querySelectorAll('.yield');
for (let i = 0; i < td.length; i++) {
  if (Number(td[i].innerHTML) < 0) {
    td[i].style.color = 'red';
  } else if (Number(td[i].innerHTML) > 0) {
    td[i].style.color = 'green';
  }
}
var ty = document.getElementById('tot_yield');
if (Number(ty.innerHTML) < 0) {
    ty.style.color = 'red';
  } else if (Number(ty.innerHTML) > 0) {
    ty.style.color = 'green';
  }