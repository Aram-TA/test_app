function disableScroll() {
	document.body.style.overflow = "hidden"
}

function enableScroll() {
	document.body.style.overflow = ""
}

const openWindow = async function (event) {
	event.preventDefault()

	const response = await fetch(event.target.getAttribute("href"))

	if (!response.ok) {
		throw new Error("Failed to fetch.")
	}

	const content = await response.text()
	const element = document.getElementById("readPost")

	element.innerHTML = content
	element.style.display = "flex"

	disableScroll()
	addEventToClose()
}

const addEventToReadPost = function () {
	const readingLinks = document.querySelectorAll("a.reading")
	readingLinks.forEach(link => link.addEventListener("click", openWindow))
}

const closeWindow = function (event) {
	try {
		event.preventDefault()

		const element = document.getElementById("readPost")

		element.style.display = "none"
		element.innerHTML = ""

		enableScroll()
		addEventToReadPost()
	} catch (error) {
		throw new Error(error)
	}
}

const addEventToClose = function () {
	document.getElementById("close").addEventListener("click", closeWindow)
}

document.addEventListener("DOMContentLoaded", () => {
	addEventToReadPost()
})
