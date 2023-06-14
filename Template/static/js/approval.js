// Get the modal element
var modal = document.getElementById('myModal');

// Get the button that opens the modal
var btn = document.getElementById('openModalBtn');

// Get the <span> element that closes the modal
var closeBtn = document.getElementsByClassName('close')[0];

// When the user clicks the button, open the modal
btn.onclick = function () {
  modal.style.display = 'block';
};

// When the user clicks on <span> (x), close the modal
closeBtn.onclick = function () {
  modal.style.display = 'none';
};

// When the user clicks outside the modal, close it
window.onclick = function (event) {
  if (event.target == modal) {
    modal.style.display = 'none';
  }
};

// Handle form submission
var approvalForm = document.getElementById('approvalForm');
approvalForm.onsubmit = function (e) {
  e.preventDefault(); // Prevent form submission

  var approvalStatus = document.getElementById('approvalStatus').value;
  var comment = document.getElementById('comment').value;

  // Perform further actions with the approval status and comment
  // For example, you can send an AJAX request to update the backend

  // Close the modal
  modal.style.display = 'none';
};

const checkboxes = document.querySelectorAll('input[type="checkbox"]');

checkboxes.forEach((checkbox) => {
  checkbox.addEventListener('change', () => {
    if (checkbox.checked) {
      checkboxes.forEach((cb) => {
        if (cb !== checkbox) {
          cb.checked = false;
        }
      });
    }
  });
});

// Get the cancel button element
var cancelBtn = document.querySelector('.cancelBtn');

// When the user clicks the cancel button, close the modal
cancelBtn.addEventListener('click', function () {
  modal.style.display = 'none';
});
