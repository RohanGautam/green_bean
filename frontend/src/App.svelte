<script lang="ts">
  // import svelteLogo from "./assets/svelte.svg";
  import greenBeanLogo from "/green_bean.svg";
  // import Counter from "./lib/Counter.svelte";

  interface ChatMessage {
    message: string;
    from: "user" | "ai";
  }

  let user_country: string = "Singapore";
  let user_business_name: string = "";
  let user_industry: string = "";
  let latest_news_data = "";
  let chat_messages: ChatMessage[] = [];
  let user_current_chat_text = "";
  // TODO : make tweakable environment variable for easier deployment?
  const API_BASE_URL = "http://127.0.0.1:8000";

  const country_namespace_map = {
    Singapore: "singapore",
    India: "india",
    USA: "usa",
  };
  const country_suggested_qn_map = {
    Singapore: [
      "How can my tech company better abide by regulations here?",
      "What energy policies does my company need to compy with?",
      "Do I need to make sustainability reports every year?",
    ],
    India: [
      "I have a textile manufacturing company. What policies should I keep in mind?",
      "What does Corporate social responsibility require me to do?",
      "What sustainability policies are in place here?",
    ],
    USA: [
      "How can my tech company better abide by regulations here?",
      "What energy policies does my company need to compy with",
      "Are there any penalties for non-complaince with sustainability regulations?",
    ],
  };

  let show_loading = false;

  // utility functions
  function sleep(ms) {
    return new Promise((resolve) => setTimeout(resolve, ms));
  }
  function serialize(obj) {
    let str = [];
    for (let p in obj)
      if (obj.hasOwnProperty(p)) {
        str.push(encodeURIComponent(p) + "=" + encodeURIComponent(obj[p]));
      }
    return str.join("&");
  }
  // main functions
  function get_latest_news() {
    // no form validation, bless our soul
    let namespace = country_namespace_map[user_country];
    const url = `${API_BASE_URL}/latest_news/${namespace}`;
    // const url = `${API_BASE_URL}`;
    show_loading = true;
    console.log(url);
    // for testing
    // sleep(2000).then(() => {
    //   let dummy_response =
    //     "Lorem ipsum dolor sit amet, consectetur adipiscing elit.\n\n Maecenas mollis leo ipsum, sit amet feugiat orci fringilla sed. Praesent at posuere ligula. Nullam consequat pretium facilisis. Phasellus vel auctor augue. Ut eget fringilla odio. Morbi enim odio, posuere ac eros eu, mollis auctor risus. Aenean justo neque, egestas vitae lectus iaculis, ultrices molestie nisl. Maecenas facilisis dolor vitae neque pharetra fringilla. Fusce sit amet libero magna. Ut tincidunt quam at fermentum sodales. Phasellus pellentesque tempus nibh et mollis. Pellentesque et lectus ultricies, venenatis eros sed, porta nibh. Integer porta odio rutrum est accumsan feugiat. Vestibulum consequat lectus ac diam consectetur laoreet. In lorem sem, egestas ut sem vitae, egestas lacinia sapien. Donec bibendum id leo et porta.";
    //   show_loading = false;
    //   latest_news_data = dummy_response;
    // });

    fetch(url)
      .then((response) => response.json())
      .then((v) => {
        console.log(v);
        latest_news_data = v["content"];
        show_loading = false;
      })
      .catch((err) => {
        console.log("error encountered");
        console.log(err);
        show_loading = false;
        return [];
      });
  }

  function on_user_chat_send(e: any) {
    e.preventDefault();
    // read and show user data
    let data = new FormData(e.currentTarget);
    let textval = Object.fromEntries(data)["chatText"] as string;
    console.log(textval);
    chat_messages = [...chat_messages, { message: textval, from: "user" }];
    user_current_chat_text = ""; // clear text field
    // get AI response
    let serialized_query = serialize({ q: textval });
    let namespace = country_namespace_map[user_country];
    const url = `${API_BASE_URL}/qa/${namespace}?${serialized_query}`;
    console.log(url);
    // sleep(2000).then(() => {
    //   chat_messages = [
    //     ...chat_messages,
    //     { message: "hey there handsome", from: "ai" },
    //   ];
    // });
    fetch(url)
      .then((response) => response.json())
      .then((v) => {
        let content = v["content"];
        chat_messages = [...chat_messages, { message: content, from: "ai" }];
      })
      .catch((e) => {
        console.log("error!");
        console.log(e);
      });
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
          <span class="label-text"
            >What is the name of your business? (optional)</span
          >
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
          <span class="label-text"
            >What industry is your business in?(optional)</span
          >
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
      Get to know the latest sustainability regulation news for {user_country}
    </p>
    <p class="text-md">
      Specially crafted by an autonomous agent for you 🤖❤️ (this might take
      around 30-40s maximum)
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

  <div class="bg-base-200 p-8 m-2 rounded-md">
    <p class="text-xl">
      Deepen your understanding of {user_country}'s sustainability regulations
    </p>
    <div>
      <span>Corpus: </span>
      <span class="badge">source</span>
      <span class="badge">source</span>
      <span class="badge">source</span>
      <span class="badge">source</span>
      <span class="badge">source</span>
    </div>
    <div class="grid-container grid grid-cols-5 gap-2">
      <div
        class="bg-base-300 rounded-md p-4 overflow-scroll flex flex-col-reverse h-96 col-span-4"
      >
        <div>
          {#each chat_messages as message, i}
            {#if message.from == "ai"}
              <div class="chat chat-start">
                <div class="chat-bubble break_at_newlines">
                  {message.message}
                </div>
              </div>
            {:else}
              <div class="chat chat-end">
                <div class="chat-bubble">{message.message}</div>
              </div>
            {/if}
          {/each}

          <form class="form-control w-full mt-4" on:submit={on_user_chat_send}>
            <input
              type="text"
              name="chatText"
              placeholder="Type here"
              class="input input-bordered w-full"
              bind:value={user_current_chat_text}
            />
            <!-- svelte-ignore a11y-label-has-associated-control -->
            <label class="label">
              <span class="label-text" />
              <span class="label-text">
                Press <kbd class="kbd kbd-sm">Enter</kbd> to Send
              </span>
            </label>
          </form>
        </div>
      </div>
      <div class="bg-base-300 rounded-md col-span-1 p-2">
        <p>Your query</p>
        <div class="bg-base-100 p-2 rounded-md">
          {user_current_chat_text ? user_current_chat_text : "-"}
        </div>
        <div class="divider">Or try:</div>
        <!-- svelte-ignore a11y-no-static-element-interactions -->
        {#each country_suggested_qn_map[user_country] as suggestion}
          <!-- svelte-ignore a11y-click-events-have-key-events -->
          <div
            class="bg-base-100 p-2 rounded-md mt-2"
            on:click={() => {
              user_current_chat_text = suggestion;
            }}
          >
            {suggestion}
          </div>
        {/each}
      </div>
    </div>
  </div>
  <!-- TODO: add footer -->
</main>

<style>
  .break_at_newlines {
    white-space: pre-line;
  }
</style>
