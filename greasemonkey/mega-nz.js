// ==UserScript==
// @name         Sort Mega.nz files by size and Bookmark
// @namespace    http://tampermonkey.net/
// @version      0.3
// @description  Add sortbysize button on mega.nz
// @author       Orange soda and JethaLal_420
// @match        https://mega.nz/folder/*
// @icon         https://www.google.com/s2/favicons?domain=mega.nz
// @grant        none
// @updateURL    https://raw.githubusercontent.com/MittalMakwana/automation_scripts/master/greasemonkey/mega-nz.js
// @downloadURL  https://raw.githubusercontent.com/MittalMakwana/automation_scripts/master/greasemonkey/mega-nz.js
// ==/UserScript==

(function () {
    "use strict";
    const AUTH_TOKEN = 'dccba67d-e10a-4db0-9148-5229dc7c6684';
    const CHECK_DIR_ID = '28212003'; // Collection id to store the Bookmark
    const BOOKMARK_TAGS = ['xxx', 'mega'];

    const createBtn = (btnName, id) => {
        var button = document.createElement("BUTTON");
        button.innerHTML = btnName;
        button.id = id;
        return button;
    };

    const insertBtn = () => {
        clearInterval(intervalId);
        var parentNode = document.getElementsByClassName("fm-breadcrumbs-wrapper")[0];
        var childNode = document.getElementsByClassName("fm-breadcrumbs-block")[0];
        var bookMarkBtn = createBtn("Bookmark This", "bookmark");
        parentNode.insertBefore(bookMarkBtn, childNode);
        checkBookMark();
        bookMarkBtn.onclick = addBookmark;
    };

    const checkDataLoaded = () => {
        var listViewBtn = document.getElementsByClassName("listing-view")[0];
        var blockViewBtn = document.getElementsByClassName("block-view")[0];
        if (listViewBtn && blockViewBtn) {
            clearInterval(intervalId);
            return true;
        }
    };

    let intervalId = setInterval(() => {
        if (checkDataLoaded() && !document.getElementById("bookmark")) {
            insertBtn();
        }
    }, 1000);

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
        }).catch(error => console.log('error', error));
    };
})();