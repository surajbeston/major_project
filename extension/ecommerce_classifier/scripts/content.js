
setTimeout(async () => {
    var title = document.querySelector(".pdp-mod-product-badge-title").innerText

    var description = document.querySelector(".pdp-product-highlights").innerText

    var results = await axios.post('https://ecommerce-classifier.fly.dev/categorize', { "title": title})
    console.log(results)
    

    const response = await chrome.runtime.sendMessage(results.data);
    console.log(response);

}, 2000)
