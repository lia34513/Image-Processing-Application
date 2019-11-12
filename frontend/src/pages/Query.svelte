<script>
  import { onMount } from 'svelte';

  import { GET } from '../utils';

  let images = [];

  let maxWidth = 5000;
  let minArea = 1;
  let minBitsPerPix = 1;
  
  const getImages = async () => {
    try {
      const res = await GET('query', { max_width: maxWidth, min_area: minArea, min_bits_per_pix: minBitsPerPix });
      console.log('/api/query => Response ->', res);
      if (Array.isArray(res)) images = res;
    } catch (error) {
      console.error('/api/query => Response ->', error);
    }
  };

	onMount(() => { getImages(); });
</script>


<div class="content">
  <div class="field">
    <label class="label">Max Width (Pixels): {maxWidth}</label>
    <div class="control">
      <input class="input is-small" type=number on:change={() => getImages()} bind:value={maxWidth} min=0 max=5000>
      <input type=range class="full-width" on:mouseup={() => getImages()} bind:value={maxWidth} min=0 max=5000>
    </div>
  </div>
  <div class="field">
    <label class="label">Min Area (Pixels): {minArea}</label>
    <div class="control">
      <input class="input is-small" type=number on:change={() => getImages()} bind:value={minArea} min=0 max=10000000>
      <input type=range class="full-width" on:mouseup={() => getImages()} bind:value={minArea} min=0 max=10000000>
    </div>
  </div>
  <div class="field">
    <label class="label">Min Bits Per Pixel: {minBitsPerPix}</label>
    <div class="control">
      <input class="input is-small" type=number on:change={() => getImages()} bind:value={minBitsPerPix} min=0 max=32>
      <input type=range class="full-width" on:mouseup={() => getImages()} bind:value={minBitsPerPix} min=0 max=32>
    </div>
  </div>
  <div class="field">
    <label class="label">Matching Images: {images.length}</label>
  </div>
  <table>
    <thead>
      <tr>
        <td>#</td>
        <td>Preview</td>
        <td>File Name</td>
      </tr>
    </thead>
    <tbody>
      {#each images as i, index}
        <tr>
          <td>{index + 1}</td>
          <td>
            <img src="/api/filter/{i.split('.')[0]}/original" alt={i} style="max-width: 100px;"/>
          </td>
          <td>{i}</td>
        </tr>
      {/each}
    </tbody>
  </table>
</div>
