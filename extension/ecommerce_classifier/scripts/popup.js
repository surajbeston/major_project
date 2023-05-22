chrome.runtime.onMessage.addListener(
    function (data, sender, sendResponse) {


        var category = data['category']
        var sub_category = data['sub_category']
        var brand = data['brand']

        if (category) {
            
            document.getElementById("category").innerText =  `Category: ${category}`
            document.getElementById("category-input").value = category
            
        }

        if (sub_category) {
            document.getElementById("sub_category").innerText = `Sub Category: ${sub_category}`
            document.getElementById("sub-category-input").value = sub_category
        }

        if (brand) {
            document.getElementById("brand").innerText = `Brand: ${brand}`
            document.getElementById("brand-input").value = brand
        }
        sendResponse({ received: sub_category });
    }
);



document.getElementById("category").addEventListener("click", () => {
    var category = document.getElementById("category-input").value
    var url = `https://ecommerce-classifier.fly.dev/filter-by-category/${category.toLowerCase().replaceAll('&', '').replaceAll('.', '').replaceAll(',', '').replaceAll(' ', '-')}`
    chrome.tabs.create({ url });
})

document.getElementById("sub_category").addEventListener("click", () => {
    var sub_category = document.getElementById("sub-category-input").value
    var url = `https://ecommerce-classifier.fly.dev/filter-by-sub-category/${sub_category.toLowerCase().replaceAll('&', '').replaceAll('.', '').replaceAll(',', '').replaceAll(' ', '-')}`
    chrome.tabs.create({ url });
})


document.getElementById("brand").addEventListener("click", () => {
    var brand = document.getElementById("brand-input").value
    var url = `https://ecommerce-classifier.fly.dev/filter-by-brand/${brand}`
    chrome.tabs.create({ url });
})
