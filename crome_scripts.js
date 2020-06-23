/****

Use the following script to Remove all the Manage search engine in google crom
It removes any search enginge that contains  a '.'
To use the script
1) Navigate to chrome://settings/
2) Press Command+Option+J (Console mode)
3) In the console prompt pase the script

****/
settings.SearchEnginesBrowserProxyImpl.prototype.getSearchEnginesList().then(function(val) {
        val.others.sort(function(a, b) { return b.modelIndex - a.modelIndex; });
        val.others.forEach(function(engine) {
            if(engine.keyword.includes('.')){
            settings.SearchEnginesBrowserProxyImpl.prototype.removeSearchEngine(engine.modelIndex);
            }
        });
    });
