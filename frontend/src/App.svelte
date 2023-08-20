<script lang="ts">
  // import svelteLogo from "./assets/svelte.svg";
  import greenBeanLogo from "/green_bean.svg";
  // import Counter from "./lib/Counter.svelte";

  let user_country: string = "Singapore";
  let user_business_name: string = "";
  let user_industry: string = "";
</script>

<main>
  <div class="navbar bg-primary">
    <div class="navbar-start" />
    <div class="navbar-center text-primary-content">
      <img src={greenBeanLogo} alt="logo" height="50" width="50" />
      <a class="btn btn-ghost normal-case text-xl" href="/">The Green Bean</a>
    </div>
    <div class="navbar-end text-primary-content" />
  </div>

  <div class=" bg-base-200 p-8 m-2 rounded-md">
    <p class="text-xl">Let's get to know you!</p>
    <div class="flex flex-row justify-evenly">
      <div class="form-control w-full max-w-xs">
        <!-- svelte-ignore a11y-label-has-associated-control -->
        <label class="label">
          <span class="label-text">Pick your location of interest</span>
        </label>
        <select class="select select-bordered" bind:value={user_country}>
          <option selected>Singapore</option>
          <option>India</option>
          <option>USA</option>
        </select>
      </div>
      <div class="form-control w-full max-w-xs">
        <!-- svelte-ignore a11y-label-has-associated-control -->
        <label class="label">
          <span class="label-text">What is the name of your business?</span>
        </label>
        <input
          type="text"
          placeholder="Type here"
          class="input input-bordered w-full max-w-xs"
          bind:value={user_business_name}
        />
      </div>
      <div class="form-control w-full max-w-xs">
        <!-- svelte-ignore a11y-label-has-associated-control -->
        <label class="label">
          <span class="label-text">What industry is your business in?</span>
        </label>
        <input
          type="text"
          placeholder="Type here"
          class="input input-bordered w-full max-w-xs"
          bind:value={user_industry}
        />
      </div>
    </div>
  </div>
  <!-- <p>{user_country}, {user_business_name}, {user_industry}</p> -->

  <!-- TODO: add footer -->
</main>
