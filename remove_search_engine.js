
// Google Chrome saves lots of Other Search Engines from websites 
// The following javascript allows you to remove search engine 
// Go to chrome://settings/searchEngines, hit F12 and paste this into the Console tab:

settings.SearchEnginesBrowserProxyImpl.prototype.getSearchEnginesList().then(function(val) {
  val.others.sort(function(a, b) { return b.modelIndex - a.modelIndex; });
  val.others.forEach(function(engine) {
  if(engine.keyword.includes('.')) {
    settings.SearchEnginesBrowserProxyImpl.prototype.removeSearchEngine(engine.modelIndex);
	}
 });
});
