// 결제하기 버튼 클릭 시 모달 창 보이기
document.getElementById('paymentButton').addEventListener('click', function () {
  document.getElementById('paymentModal').style.display = 'block';
});

// 확인 버튼 클릭 시 동작
document
  .getElementById('confirmButton')
  .addEventListener('click', function (event) {
    event.preventDefault();

    var rejectCheckbox = document.getElementById('rejectCheckbox');
    var approveCheckbox = document.getElementById('approveCheckbox');

    if (rejectCheckbox.checked) {
      document.getElementById('paymentForm').submit();
    } else if (approveCheckbox.checked) {
      document.getElementById('paymentForm').submit();
    } else {
    }
  });

var modal = document.getElementById('paymentModal');
var cancelModalButton = document.getElementById('cancelModalButton');

cancelModalButton.onclick = function () {
  modal.style.display = 'none';
};

confirmButton.onclick = function (event) {
  if (!rejectCheckbox.checked && !approveCheckbox.checked) {
    event.preventDefault();
    alert('반려 또는 결제를 선택해야 합니다.');
  }
};