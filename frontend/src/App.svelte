<script src="http://localhost:35729/livereload.js">
  import { Router, Route } from 'svero';

  import { currentPath } from './store';

  import Layout from './components/Layout.svelte';

  // Pages
  import Introduction from './pages/Introduction.svelte';
  import All from './pages/All.svelte';
  import Query from './pages/Query.svelte';
  import Filter from './pages/Filter.svelte';
  import Log from './pages/Log.svelte';

  $currentPath = window.location.pathname;
  const updatePath = () => { $currentPath = window.location.pathname; };
</script>

<svelte:window on:popstate={updatePath}/>
<Layout>
	<Router>
    <Route exact path="/" component={Introduction} />
    <Route path="/all" component={All} />
    <Route path="/query" component={Query} />
    <Route path="/filter" component={Filter} />
    <Route path="/log" component={Log} />
  </Router>
</Layout>
