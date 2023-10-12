document.getElementById('paymentButton').addEventListener('click', function () {
  document.getElementById('paymentModal').style.display = 'block';
});

document
  .getElementById('reportCheckbox')
  .addEventListener('change', function () {
    const reportSelect = document.getElementById('reportSelect');
    if (this.checked) {
      reportSelect.style.display = 'inline-block';
    } else {
      reportSelect.style.display = 'none';
    }
  });

var rejectCheckbox = document.getElementById('rejectCheckbox');
var approveCheckbox = document.getElementById('approveCheckbox');
var reportCheckbox = document.getElementById('reportCheckbox');
var modal = document.getElementById('paymentModal');
var cancelModalButton = document.getElementById('cancelModalButton');

document
  .getElementById('confirmButton')
  .addEventListener('click', function (event) {
    if (
      !rejectCheckbox.checked &&
      !approveCheckbox.checked &&
      !reportCheckbox.checked
    ) {
      event.preventDefault();
      alert('반려, 결재 또는 보고를 선택해야 합니다.');
    } else {
      document.getElementById('paymentForm').submit();
    }
  });

cancelModalButton.onclick = function () {
  modal.style.display = 'none';
};
