<script lang="ts">
  // import svelteLogo from "./assets/svelte.svg";
  import greenBeanLogo from "/green_bean.svg";
  // import Counter from "./lib/Counter.svelte";
</script>

<main>
  <div class="navbar bg-primary text-primary-content">
    <img src={greenBeanLogo} alt="logo" height="50" width="50" />
    <div class="navbar-center">
      <a class="btn btn-ghost normal-case text-xl" href="/">The Green Bean</a>
    </div>
  </div>
  <button
    class="inline-block cursor-pointer rounded-md bg-gray-800 px-4 py-3 text-center text-sm font-semibold uppercase text-white transition duration-200 ease-in-out hover:bg-gray-900"
  >
    Button
  </button>

  <!-- TODO: add footer -->
</main>
