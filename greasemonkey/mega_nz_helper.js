// ==UserScript==
// @name         Sort Mega.nz files by size and Bookmark
// @namespace    http://tampermonkey.net/
// @version      0.3
// @description  Add sortbysize button on mega.nz
// @author       Orange soda and JethaLal_420
// @match        https://mega.nz/folder/*
// @icon         https://www.google.com/s2/favicons?domain=mega.nz
// @grant        none
// ==/UserScript==

(function () {
    "use strict";
    const AUTH_TOKEN = 'TOKEN';
    const CHECK_DIR_ID = 'Folder ID';
    const BOOKMARK_TAGS = ['tag1', 'tag2'];


    var listViewBtn, blockViewBtn;

    const createBtn = (btnName, id) => {
        var button = document.createElement("BUTTON");
        button.innerHTML = btnName;
        button.id = id;
        return button;
    };

    const checkDataLoaded = () => {
        listViewBtn = document.getElementsByClassName("listing-view")[0];
        blockViewBtn = document.getElementsByClassName("block-view")[0];
    };

    const sortBySize = () => {
        listViewBtn.click();
        console.log("List View btn Clicked");
        var sizeBtn = document.getElementsByClassName("size")[0];
        setTimeout(() => {
            sizeBtn.click();
            sizeBtn.click();
        }, 500);
        blockViewBtn.click();
        console.log("Block View btn Clicked");
    };

    const addBookmark = () => {

        let preTags = document.getElementsByClassName("not-loading selectable-txt")
        let p = preTags[0];
        var myHeaders = new Headers();
        myHeaders.append("Authorization", "Bearer "+AUTH_TOKEN);
        myHeaders.append("Content-Type", "application/json");

        var raw = JSON.stringify({
            "link": document.URL,
            "title": p.innerText,
            "tags": BOOKMARK_TAGS,
            "collectionId": CHECK_DIR_ID
        });

        var requestOptions = {
            method: 'POST',
            headers: myHeaders,
            body: raw,
            redirect: 'follow'
        };

        fetch("https://api.raindrop.io/rest/v1/raindrop", requestOptions)
            .then(response => {
            // response.text()
            if (response.ok) {
                document.getElementById("bookmark").innerText="Done";
                document.getElementById("bookmark").disabled = true;
            }
            else
            {
                throw `error with status ${response.status}`;
            }
        })
            .then(result => console.log(result))
            .catch(error => console.log('error', error));

    };

    const checkBookMark = () => {
        var myHeaders = new Headers();
        myHeaders.append("Authorization", "Bearer "+ AUTH_TOKEN);

        var requestOptions = {
            method: 'GET',
            headers: myHeaders,
            redirect: 'follow'
        };

        fetch("https://api.raindrop.io/rest/v1/raindrops/"+CHECK_DIR_ID, requestOptions)
            .then(response => response.text())
            .then(result => {
            var data = JSON.parse(result)
            var findURL = data.items.find((item) => {
                return item.link == document.URL
            })
            console.log(findURL)
            if (data.result && findURL) {
                document.getElementById("bookmark").innerText="Already BookMark";
                document.getElementById("bookmark").disabled = true;
            }
        })
            .catch(error => console.log('error', error));
    };

    let intervalId = setInterval(() => {
        checkDataLoaded();

        if (listViewBtn && blockViewBtn) {
            insertBtn();
        }
    }, 1000);

    const insertBtn = () => {
        clearInterval(intervalId);

        var parentNode = document.getElementsByClassName("fm-breadcrumbs-wrapper")[0];
        var childNode = document.getElementsByClassName("fm-breadcrumbs-block")[0];
        var btn = createBtn("Sort_By_Size", "sortbysize");
        var bookMarkBtn = createBtn("Bookmark This", "bookmark");
        parentNode.insertBefore(btn, childNode);
        parentNode.insertBefore(bookMarkBtn, btn);
        checkBookMark();
        btn.onclick = sortBySize;
        bookMarkBtn.onclick = addBookmark;
    };
})();