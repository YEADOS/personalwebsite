chrome.tabs.onUpdated.addListener((tabId, changeInfo, tab) => {
    if (changeInfo.url && changeInfo.url.includes("https://leetcode.com/")) {
      fetch("http://nyeados.pythonanywhere.com/tracker/update_streak", { method: "POST" })
        .then(response => console.log("Streak updated"))
        .catch(error => console.error("Error updating streak:", error));
    }
  });
  