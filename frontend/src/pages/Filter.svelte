<script>
  import { onMount } from 'svelte';

  import { GET } from '../utils';

  let images = [];
  let selectedImageName = null;
  let selectedFilter = 'original';
  let value = 1;
  
  const getAllImages = async () => {
    try {
      const res = await GET('all');
      console.log('/api/all => Response ->', res);
      if (Array.isArray(res)) images = res;
    } catch (error) {
      console.error('/api/all => Error ->', error);
    }
  };

	onMount(() => { getAllImages(); });
</script>


<div class="content">
  <div class="field">
    <label class="label">Image</label>
    <div class="control">
      <div class="select">
        <select bind:value={selectedImageName}>
          <option value={null}>None</option>
          {#each images as i}
            <option value={i.imagename}>{i.imagename}</option>
          {/each}
        </select>
      </div>
      <button class="button" on:click={getAllImages}>Refresh Image List</button>
    </div>
  </div>
  <div class="field">
    <label class="label">Filter</label>
    <div class="control">
      <div class="select">
        <select bind:value={selectedFilter}>
          <option value="original">Original</option>
          <option value="lowpass">Lowpass</option>
          <option value="crop">Crop</option>
          <option value="dx">dx</option>
          <option value="dy">dy</option>
          <option value="downsample">Downsample</option>
          <option value="rotate">Rotate</option>
        </select>
      </div>
    </div>
  </div>
  <div class="field">
    <label class="label">Value (Query Param)</label>
    <div class="control">
      <input class="input" type=number bind:value={value}>
    </div>
  </div>
</div>

{#if selectedImageName}
  <p>{selectedImageName}</p>
  <img src="/api/filter/{selectedImageName.split('.')[0]}/{selectedFilter}?value={value}" alt={selectedImageName}/>
{:else}
  <p>Select an image</p>
{/if}
