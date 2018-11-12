Promise.all(UI.panels.network._networkLogView._dataGrid._rootNode._flatNodes
    .map(node => node._request.contentData()
    .then(data => safelyParseJSON(data.content))))
    .then(console.log);
