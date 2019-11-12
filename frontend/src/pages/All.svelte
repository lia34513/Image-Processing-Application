<script>
  import { onMount } from 'svelte';

  import { GET, bytesToSize } from '../utils';

  let images = [];
  
  const getAllImages = async () => {
    try {
      const res = await GET('all');
      console.log('/api/all => Response ->', res);
      if (Array.isArray(res)) images = res;
    } catch (error) {
      console.error('/api/all => Error ->', error);
    }
  };

  const populateDatabase = async () => {
    try {
      const res = await GET('populate_database');
      console.log('/api/populate_database => Response ->', res);
      if (Array.isArray(res)) images = res;
    } catch (error) {
      console.error('/api/populate_database => Error ->', error);
    }
  };

  const getImagePreview = async (imageName) => {
    try {
      const res = await GET(`image/${imageName}/downsample`, { value: 1 });
      console.log(`/api/image/${imageName}/downsample => Response ->`, res);
    } catch (error) {
      console.error(`/api/image/${imageName}/downsample => Error ->`, error);
    }
  };

	onMount(() => {
    getAllImages();
    getImagePreview('city');
  });
</script>

<div class="content">
  <button class="button" on:click={populateDatabase}>Populate Database</button>
  <button class="button" on:click={getAllImages}>Refresh Image List</button>
  <p>Total Images: {images.length}</p>
  <table>
    <thead>
      <tr>
        <td>#</td>
        <td>Preview</td>
        <td>File Name</td>
        <td>File Size</td>
        <td>Width</td>
        <td>Height</td>
        <td>Area</td>
      </tr>
    </thead>
    <tbody>
      {#each images as i, index (i.imagename)}
        <tr>
          <td>{index + 1}</td>
          <td>
            <img src="/api/filter/{i.imagename.split('.')[0]}/original" alt={i.imageName} style="max-width: 100px;"/>
          </td>
          <td>{i.imagename}</td>
          <td>{bytesToSize(i.size)}</td>
          <td>{i.width}</td>
          <td>{i.height}</td>
          <td>{i.area.toLocaleString()}</td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>
