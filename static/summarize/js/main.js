$(document).ready(() => {
    const text = $('#text');
    const fileInput = $('#fileInput');

    $('.btn-upload').click(() => {
        fileInput.click();
    });

    $('#text').on('input', () => {
        if (text.val().length > 1024) {
            text.val(text.val().substring(0, 1024));
        }
        $('#text-length span').text(text.val().length + '/1024 characters');
    });

    $('.btn-summarize').click((event) => {
        const button = $(event.currentTarget);
        if (text.val().length === 0) {
            alert('Please enter some text to summarize.');
            return;
        }
        button.prop('disabled', true);
        button.html('<span class="spinner-border spinner-border-sm" role="status" aria-hidden="true"></span> Summarizing...');
        fetch(window.location.origin + '/predict', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text_input: text.val() })
        })
            .then(response => response.json())
            .then(response => {
                $('#summarized').text(response.data);
                button.prop('disabled', false);
                button.text('Summarize');
            });
    });

    fileInput.change((event) => {
        const file = event.currentTarget.files[0];
        if (file) {
            const fileName = file.name.toLowerCase();
            if (fileName.endsWith('.txt')) {
                const reader = new FileReader();
                reader.onload = (event) => {
                    text.val(event.target.result);
                };
                reader.readAsText(file);
            } else if (fileName.endsWith('.docx') || fileName.endsWith('.doc')) {
                mammoth.extractRawText({ arrayBuffer: file })
                    .then(result => {
                        text.val(result.value.replace(/\s+/g, ' '));
                    })
            } else {
                alert("Unsupported file format. Please select a .txt, .docx, or .doc file.");
            }
        }
    });
});