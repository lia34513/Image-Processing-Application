<script>
  import { onMount } from 'svelte';

  import { GET, bytesToSize } from '../utils';

  let logs = [];

  const getAllLogs = async () => {
    try {
      const res = await GET('all');
      console.log('/api/log => Response ->', res);
      if (Array.isArray(res)) logs = res;
    } catch (error) {
      console.error('/api/log => Error ->', error);
    }
  };

	onMount(() => {
    getAllLogs();
  });
</script>

<div class="content">
  <table>
    <thead>
      <tr>
        <td>#</td>
        <td>File Name</td>
        <td>Filter Type</td>
        <td>Request Timestamp</td>
        <td>Processing Time</td>
      </tr>
    </thead>
    <tbody>
      {#each logs as i, index (i.filename)}
        <tr>
          <td>{index + 1}</td>
          <td>{i.filename}</td>
          <td>{i.filtertype}</td>
          <td>{i.request_timestamp}</td>
          <td>{i.processing_time}</td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>