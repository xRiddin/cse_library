document.getElementById('lib_issue_id').addEventListener('input', function() {
    var id = this.value;
            console.log("fetching", id)

    fetch('/get_user_details/' + id)
        .then(response => response.json())
        .then(data => {
            // Update the fields with the returned data
            console.log(data)
            document.getElementById('name-field').innerHTML = data.name;
            document.getElementById('email-field').innerHTML = data.email;
            document.getElementById('phone-field').innerHTML = data.phone;
            document.getElementById('book-field').innerHTML = data.issued_book;
            document.getElementById('fine-field').innerHTML = data.fine;

            // Add similar lines for other fields
        });
});