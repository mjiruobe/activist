<template>
  <div
    class="flex flex-col w-full px-3 py-4 md:flex-row card-style md:grow lg:px-5 md:py-3"
  >
    <BtnAction
      class="hidden mt-1 md:flex h-min"
      :cta="true"
      :counter="discussion.upVoters"
      fontSize="sm"
      leftIcon="bi:arrow-up"
      iconSize="1.25em"
      ariaLabel="components.btn-action.upvote-discussion-aria-label"
    />
    <div class="flex-col space-y-3 md:pl-4 lg:pl-6 md:space-y-4 md:grow">
      <div class="flex flex-col justify-between md:flex-row">
        <div class="flex flex-col md:flex-row md:items-center md:space-x-4">
          <div class="flex justify-between w-full">
            <h2 class="w-full font-bold responsive-h3">
              {{ discussion.title }}
            </h2>
            <div class="flex items-center space-x-3 md:hidden md:w-fit">
              <MetaTagMembers
                :members="discussion.participants"
                :label="label"
              />
              <MetaTag
                iconName="bi:chat-left"
                :value="String(discussion.messages)"
                :label="label"
              />
            </div>
          </div>
          <div class="flex space-x-2">
            <BtnAction
              class="flex mt-1 md:hidden"
              :cta="true"
              :label="discussion.upVoters"
              fontSize="sm"
              leftIcon="bi:arrow-up"
              iconSize="1.25em"
              ariaLabel="components.btn-action.upvote-discussion-aria-label"
            />
            <BtnAction
              class="flex mt-1"
              :cta="true"
              :label="discussion.category"
              fontSize="sm"
              iconSize="1.25em"
              ariaLabel="components.btn-action.filter-discussion-category-aria-label"
            />
          </div>
        </div>
        <div
          class="items-center hidden w-full space-x-3 md:flex md:w-fit lg:space-x-5"
        >
          <MetaTagMembers :members="discussion.participants" :label="label" />
          <MetaTag
            iconName="bi:chat-left"
            :value="String(discussion.messages)"
            :label="label"
          />
        </div>
      </div>
      <div class="flex">
        <div
          class="flex justify-center space-x-3 lg:space-x-4 md:justify-start"
        >
          <a href="/" class="flex items-center">
            <div
              class="flex items-center justify-center w-8 h-8 border rounded-full border-light-section-div dark:border-dark-section-div bg-light-content dark:bg-dark-content"
            >
              <Icon name="bi:person" size="1.5em" />
            </div>
            <p class="ml-2">{{ discussion.author }}</p>
          </a>
          <div class="flex items-center ml-2">
            <MetaTagDate :date="event?.date.toLocaleDateString()" />
            <p class="mt-0.8 ml-1">
              {{ discussion.creationDate.toLocaleDateString() }}
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import type { DiscussionEntry } from "~/types/card-discussion-entry";

defineProps<{
  isPrivate?: boolean;
  discussion: DiscussionEntry;
}>();
</script>
