/*
TODO: Add support for https://bypass.pm/bypass2?url=*
*/

const browsing = {
  name: "Brave Browser",
  profile: "Profile 1",
};

const safari = {
  name: "Safari",
};

var debug = false;

// Define regular expressions for URLs
const linkHubUrls = /^https?:\/\/(linkvertise\.com|(link-hub|link-center|link-target|direct-link)\.net)\/.*$/;
const gohubUrls = /^https:\/\/(gohub.fpc.oo.gd|fpc.oo.gd|binb.me|go.fpc.oo.gd|exe.io|cuty.io|paster.so|bunkr.sk).*$/;
const megadropz = /^https?:\/\/(www\.)?(megadropz\.com|leak-pragmatic\.com|free-leaks\.com)\/.*$/;
const megaUrls = /^https:\/\/(www\.)?mega\.nz\/.*$/;
const rentryUrls = /^https:\/\/(www\.)?rentry.co\/.*$/;
const teraboxUrls = /^https:\/\/(www\.)?(teraboxapp\.com|teraboxlink\.com|terabox\.tech|terafileshare\.com).*$/;
const pastelinesUrls = /^https?:\/\/(www\.)?rentry\.co\/.*$/;
const elitepacks = /^https?:\/\/(members\.elitepacks\.vip)(.*$)/;


module.exports = {
  defaultBrowser: "Safari",

  rewrite: [
     {
        match: (all) => {
          if (debug) {
            finicky.log(JSON.stringify(all, null, 2));
          }
          return true;
        }, // Apply the rewrite to all incoming URLs
        url: ({ url }) => {
          // Define prefixes of query parameters to remove
          const removeKeysStartingWith = ["utm_", "uta_"];
          // Define specific query parameters to remove
          const removeKeys = ["fbclid", "gclid"];
    
          const search = url.search
            .split("&")
            .map((param) => param.split("="))
            .filter(([key]) => 
              !removeKeysStartingWith.some((prefix) => key.startsWith(prefix))
            )
            .filter(([key]) => 
              !removeKeys.includes(key)
            );    
          return {
            ...url,
            search: search.map((param) => param.join("=")).join("&"),
          };
        },
      },
      {
        match: ({ url }) => {
          const pattern = /teraboxlink|teraboxapp|1024tera|terafileshare/
          if (pattern.test(url.host)) {
            return true;
          }
        },
        url: ({ url }) => {
          const id = url.pathname.split("/").pop();
          return {
            ...url,
            host: "terabox.tech",
            pathname: `/`,
            search: `url=${id}`,
          };
        },
      },
  ],

  options: {
    hideIcon: false,
    checkForUpdate: true,
  },
  handlers: [
    {
      // Open links in Brave when the option key is pressed
      // Valid keys are: shift, option, command, control, capsLock, and function.
      // Please note that control usually opens a tooltip menu instead of visiting a link
      match: () => finicky.getKeys().option,
      browser: browsing,
    },
    {
      // Open links in Brave when the option key is pressed
      // Valid keys are: shift, option, command, control, capsLock, and function.
      // Please note that control usually opens a tooltip menu instead of visiting a link
      match: () => finicky.getKeys().command,
      browser: safari,
    },
    {
      // Matches URLs from link-hub.net, link-center.net, link-target.net, direct-link.net, and linkvertise.com
      match: linkHubUrls,
      browser: browsing,
    },
    {
      // Matches URLs from gohub.fpc.oo.gd, fpc.oo.gd, binb.me, go.fpc.oo.gd, exe.io, cuty.io, paster.so, and bunkr.sk
      match: gohubUrls,
      browser: browsing,
    },
    {
      // Matches URLs from megadropz.com and leak-pragmatic.com
      match: megadropz,
      browser: browsing,
    },
    {
      // Matches URLs from mega.nz
      match: megaUrls,
      browser: browsing,
    },
    {
      // Matches URLs from rentry.co
      match: rentryUrls,
      browser: browsing,
    },
    {
      // Matches URLs from teraboxapp.com and teraboxlink.com
      match: teraboxUrls,
      browser: browsing,
    },
    {
      // Matches URLs from pastelines.com
      match: pastelinesUrls,
      browser: browsing,
    },
    {
      // Matches URLs from members.elitepacks.vip
      match: elitepacks,
      browser: browsing,
    },
  ],
};
