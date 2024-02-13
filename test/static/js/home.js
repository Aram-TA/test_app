const readPost = async function(event) {
    event.preventDefault();
    try {
        const response = await fetch(event.target.getAttribute('href'));
        if (!response.ok) {
            throw new Error('Failed to fetch.')
        }

        const content = await response.text();
        document.getElementById('html5').innerHTML = content;
        await changeGoHome();

    } catch (error) {
        throw new Error(error);
    }
}

const changeReadPost = async function() {
    const readingLinks = document.querySelectorAll('a.reading');
    readingLinks.forEach(link => link.addEventListener("click", readPost));
}

const goHome = async function(event) {
    try {
        event.preventDefault();
        const response = await fetch(window.location.href);

        if (!response.ok) {
            throw new Error('Failed to fetch.');
        }

        const content = await response.text();
        document.getElementById('html5').innerHTML = content;
        await changeReadPost();

    } catch (error) {
        throw new Error(error);
    }
}

const changeGoHome = async function() {
    document.getElementById('goHome').addEventListener('click', goHome);
    console.log("listener added");
}



document.addEventListener('DOMContentLoaded', async () => {
    try {
        await changeReadPost();
    } catch(error) {
        console.error(error);
    }
});