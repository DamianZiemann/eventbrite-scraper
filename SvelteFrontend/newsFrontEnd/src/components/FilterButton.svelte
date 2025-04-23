<script>
    export let filter = "popularity";
    export let onFilterChange = (newFilter) => {};
  </script>
  
  <div>
    <button class:active={filter === 'popularity'} on:click={() => onFilterChange('popularity')}>Beliebtheit</button>
    <button class:active={filter === 'newest'} on:click={() => onFilterChange('newest')}>Neueste</button>
    <button class:active={filter === 'oldest'} on:click={() => onFilterChange('oldest')}>Älteste</button>
    <button class:active={filter === 'abc'} on:click={() => onFilterChange('abc')}>ABC</button>
  </div>
  
  <style>
    .active {
      background-color: #0070c2;
      color: white;
    }
  </style>
  