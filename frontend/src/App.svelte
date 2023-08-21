<script lang="ts">
  // import svelteLogo from "./assets/svelte.svg";
  import greenBeanLogo from "/green_bean.svg";
  import lablabLogo from "./assets/lablab-logo.png";
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

  let show_loading = false;
  let chat_ai_loading = false;
  let use_gpt_4 = true;
  // TODO : make tweakable environment variable for easier deployment?
  // const API_BASE_URL = "http://0.0.0.0:6969";
  const API_BASE_URL = "https://green-bean-hack.onrender.com";

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
  // corpus list collected by python autonomous agent - brute force way to get about things
  const country_corpus_map = {
    India: [
      "The Water (Prevention & Control of Pollution) Act, 1974 - 2",
      "The Environment (Protection) Act, 1986",
      "The E-Waste (Management and Handling) Rules, 2011",
      "The Hazardous Waste (Management & Handling) Rules, 1989",
      "The Water (Prevention & Control of Pollution) Act, 1974",
      "The Air (Prevention & Control of Pollution) Act, 1981",
      "Solid_Waste_Management_Rules",
      "The National Green Tribunal Act, 2010",
      "The Energy Conservation Act, 2001",
      "The Plastic Waste Management Rules, 2016",
      "Corporate Social Responsibility (CSR) Rules under the Companies Act, 2013",
    ],
    Singapore: [
      "Carbon Pricing Act, 2018",
      "Sustainability Reporting - Singapore Exchange (SGX)",
      "Environmental Protection and Management Act, 1999",
      "Green Mark Certification Scheme - Building and Construction Authority (BCA)",
      "Environmental Impact Assessment website",
      "The Environmental Impact Assessment process in Singapore [research paper]",
    ],
    USA: [
      "Greenhouse Gas Reporting Programme, 2020",
      "Conflict Minerals rule, 2012",
      "EPA E-waste disposal guidelines",
      "Endangered Species Act 1973",
      "EPA Guidelines",
      "Energy Information Administration guidelines, 2022",
      "Operational Safety and Hazards Administration guide",
    ],
  };

  // utility functions
  function sleep(ms) {
    // for testing purposes only
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
    chat_ai_loading = true;
    let serialized_query = serialize({ q: textval });
    let namespace = country_namespace_map[user_country];
    let url: string;
    if (use_gpt_4) {
      url = `${API_BASE_URL}/qa/${namespace}?${serialized_query}`;
    } else {
      url = `${API_BASE_URL}/qa_fast/${namespace}?${serialized_query}`;
    }
    // console.log(url);
    // sleep(4000).then(() => {
    //   chat_messages = [
    //     ...chat_messages,
    //     { message: "hey there handsome", from: "ai" },
    //   ];
    //   chat_ai_loading = false;
    // });
    fetch(url)
      .then((response) => response.json())
      .then((v) => {
        let content = v["content"];
        chat_messages = [...chat_messages, { message: content, from: "ai" }];
        chat_ai_loading = false;
      })
      .catch((e) => {
        console.log("error!");
        console.log(e);
        chat_ai_loading = false;
      });
  }
</script>

<main>
  <div class="navbar bg-green-950">
    <div class="navbar-start" />
    <div class="navbar-center text-white">
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

  <!-- news section -->
  <div class="bg-base-200 p-8 m-2 rounded-md">
    <p class="text-2xl">
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
  <!-- chat section -->
  <div class="bg-base-200 p-8 m-2 rounded-md">
    <p class="text-2xl">
      Deepen your understanding of {user_country}'s sustainability regulations
    </p>
    <div class="mb-2">
      <span>Corpus: </span>
      {#each country_corpus_map[user_country] as src_name}
        <span class="badge">{src_name}</span>
      {/each}
      <div class="badge badge-secondary">+more</div>
    </div>
    <div>
      <input type="checkbox" class="toggle" bind:checked={use_gpt_4} />
      <span class="inline-block align-top"
        >{use_gpt_4 ? "GPT-4" : "GPT-3.5-turbo"}</span
      >
    </div>
    <div class="grid-container grid grid-cols-5 gap-2">
      <div
        class="bg-base-300 rounded-md p-4 overflow-scroll flex flex-col-reverse col-span-4 chatdiv"
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
          {#if chat_ai_loading}
            <div class="chat chat-start">
              <div class="chat-bubble">
                <span class="loading loading-bars loading-xs" />
              </div>
            </div>
          {/if}

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
          {user_current_chat_text
            ? user_current_chat_text
            : "[Enter query in the chat to get started!]"}
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
  <!-- footer -->
  <footer class="footer items-center p-4 bg-green-800 text-neutral-content">
    <div class="items-center grid-flow-col">
      <img src={greenBeanLogo} alt="logo" width="36" height="36" />
      <p>
        Copyright © 2023 - Made for the August 2023 Autonomous Agents Hackathon.
      </p>
    </div>
    <div class="grid-flow-col gap-4 md:place-self-center md:justify-self-end">
      <a href="https://github.com/RohanGautam/green_bean" target="_blank">
        <div class="tooltip tooltip-left" data-tip="Project Github">
          <svg
            class="w-10 h-10"
            fill="currentColor"
            viewBox="0 0 24 24"
            aria-hidden="true"
          >
            <path
              fill-rule="evenodd"
              d="M12 2C6.477 2 2 6.484 2 12.017c0 4.425 2.865 8.18 6.839 9.504.5.092.682-.217.682-.483 0-.237-.008-.868-.013-1.703-2.782.605-3.369-1.343-3.369-1.343-.454-1.158-1.11-1.466-1.11-1.466-.908-.62.069-.608.069-.608 1.003.07 1.531 1.032 1.531 1.032.892 1.53 2.341 1.088 2.91.832.092-.647.35-1.088.636-1.338-2.22-.253-4.555-1.113-4.555-4.951 0-1.093.39-1.988 1.029-2.688-.103-.253-.446-1.272.098-2.65 0 0 .84-.27 2.75 1.026A9.564 9.564 0 0112 6.844c.85.004 1.705.115 2.504.337 1.909-1.296 2.747-1.027 2.747-1.027.546 1.379.202 2.398.1 2.651.64.7 1.028 1.595 1.028 2.688 0 3.848-2.339 4.695-4.566 4.943.359.309.678.92.678 1.855 0 1.338-.012 2.419-.012 2.747 0 .268.18.58.688.482A10.019 10.019 0 0022 12.017C22 6.484 17.522 2 12 2z"
              clip-rule="evenodd"
            />
          </svg>
        </div>
      </a>
      <a
        href="https://lablab.ai/event/autonomous-agents-hackathon/the-green-bean"
      >
        <div
          class="tooltip tooltip-left"
          data-tip="Project team page on lablab.ai"
        >
          <img src={lablabLogo} class="w-10 h-10" alt="lablab ai logo" />
        </div>
      </a>
    </div>
  </footer>
</main>

<style>
  .break_at_newlines {
    white-space: pre-line;
  }
  .chatdiv {
    height: 600px;
  }
</style>
