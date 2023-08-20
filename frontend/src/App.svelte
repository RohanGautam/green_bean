<script lang="ts">
  // import svelteLogo from "./assets/svelte.svg";
  import greenBeanLogo from "/green_bean.svg";
  // import Counter from "./lib/Counter.svelte";

  let user_country: string = "Singapore";
  let user_business_name: string = "";
  let user_industry: string = "";
  let latest_news_data = "";
  // TODO : make tweakable environment variable for easier deployment?
  const API_BASE_URL = "http://127.0.0.1:8000";

  const country_namespace_map = {
    Singapore: "singapore",
    India: "india",
    USA: "usa",
  };

  let show_loading = false;
  function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
  function get_latest_news() {
    // no form validation, bless our soul
    let namespace = country_namespace_map[user_country];
    const url = `${API_BASE_URL}/latest_news/${namespace}`;
    // const url = `${API_BASE_URL}`;
    show_loading = true;
    console.log(url);
    // for testing
    sleep(2000).then(() => {
      let dummy_response =
        "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n\n Maecenas mollis leo ipsum, sit amet feugiat orci fringilla sed. Praesent at posuere ligula. Nullam consequat pretium facilisis. Phasellus vel auctor augue. Ut eget fringilla odio. Morbi enim odio, posuere ac eros eu, mollis auctor risus. Aenean justo neque, egestas vitae lectus iaculis, ultrices molestie nisl. Maecenas facilisis dolor vitae neque pharetra fringilla. Fusce sit amet libero magna. Ut tincidunt quam at fermentum sodales. Phasellus pellentesque tempus nibh et mollis. Pellentesque et lectus ultricies, venenatis eros sed, porta nibh. Integer porta odio rutrum est accumsan feugiat. Vestibulum consequat lectus ac diam consectetur laoreet. In lorem sem, egestas ut sem vitae, egestas lacinia sapien. Donec bibendum id leo et porta.";
      show_loading = false;
      latest_news_data = dummy_response;
    });

    // fetch(url)
    //   .then((response) => response.json())
    //   .then((v) => {
    //     console.log(v);
    //     latest_news_data = v["content"];
    //     show_loading = false;
    //   })
    //   .catch((err) => {
    //     console.log("error encountered");
    //     console.log(err);
    //     show_loading = false;
    //     return [];
    //   });
  }
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

  <div class="bg-base-200 p-8 m-2 rounded-md">
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

  <div class="bg-base-200 p-8 m-2 rounded-md">
    <p class="text-xl">
      Get to know the latest sustainability regulation news summary for {user_country}
    </p>
    <p class="text-md">
      Specially crafted by an autonomous agent for you 🤖❤️ (this might take a
      around 30-40s)
    </p>
    <button
      class="btn btn-outline"
      on:click={() => {
        get_latest_news();
      }}
    >
      Generate!
      {#if show_loading}
        <span class="loading loading-spinner" />
      {/if}
    </button>
    <button
      class="btn btn-outline"
      on:click={() => {
        latest_news_data = "";
      }}>Clear</button
    >
    <p class="break_at_newlines">{latest_news_data}</p>
  </div>
  <!-- <p>{user_country}, {user_business_name}, {user_industry}</p> -->

  <!-- TODO: add footer -->
</main>

<style>
  .break_at_newlines {
    white-space: pre-line;
  }
</style>
