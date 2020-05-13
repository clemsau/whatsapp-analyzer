document.addEventListener("DOMContentLoaded", function() {

    var uploadField = document.getElementById("file");
    var uploadFieldLabel = document.getElementById("file-label");
    var displayChartsButton = document.getElementById("display-charts-button")

    if (uploadField.files[0]) {
        uploadFieldLabel.innerHTML = uploadField.files[0].name;
    } else {
        displayChartsButton.disabled = true;
        uploadFieldLabel.innerHTML = "Select conversation file";
    }

    uploadField.onchange = function () {
        if (this.files[0].size > 1048576*10 ) {
            alert("Your file is too big (> 10 Mo)");
            this.value = "";
            displayChartsButton.disabled = true;
            uploadFieldLabel.innerHTML = "Select conversation file";
        } else {
            uploadFieldLabel.innerHTML = this.files[0].name;
            displayChartsButton.disabled = false;
        }
    };
});