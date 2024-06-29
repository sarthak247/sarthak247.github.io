---
title: "Embracing Freedom: My Journey to Creating a Personal Blog with Hugo and GitHub Pages"
description: Setup Hugo + GitHub Pages based personal blog
slug: hello-world
date: 2023-09-04 00:00:00+0000
image: /blogs/hello-world/cover.jpg
license: false
categories:
    - Website
tags:
    - Hugo
    - GitHub Pages
    - Golang
weight: 1       # You can add weight to some posts to override the default sorting (date descending)
---

## Introduction
In a world dominated by social media platforms and curated content, the idea of having a personal space on the internet has always fascinated me. A place where I can express my thoughts, share my experiences, and have complete control over what goes in and what stays out. That's why I decided to embark on a journey to create my own personal blog. This blog is my "Hello World" moment in the blogosphere, a simple yet profound beginning.

## Motivation
The motivation behind creating a personal blog stemmed from a desire for creative freedom and self-expression. Here are some reasons that fueled my motivation:

* 1. **Freedom of Expression:**
    - Unlike social media platforms with their character limits and algorithms, a personal blog gives me the freedom to express myself without constraints. I can write long-form content, delve into topics that interest me deeply, and share my unique perspective wihtout the worry of being banned or restricted.

* 2. **Ownership and Control:**
    - With a personal blog, I have complete ownership and control over my content. I don't have to worry about my content being buried in a newsfeed or subject to changing platform policies. It's my digital space, and I make the rules.

* 3. **Learning and Growth:**
    - Building and maintaining a blog is a learning experience. From setting up the technical infrastructure to crafting compelling content, I saw this as an opportunity for personal growth and development.

* 4. **Maintaining My Journal:** 
    - As I explore my way in this LLM world, I get to know a lot of new things on a daily basis and maintaining a blog is like my online catalog for everything I learn so that I can come back and visit it sometime later.

## How-To
To begin with, When I decided to embark on the journey of creating my own personal blog, one of the first decisions I had to make was choosing the right static site generator. After some research and contemplation, I found myself torn between two popular options: `Hugo` and `Jekyll`. In this blog post, I'll share my thought process, the pros and cons I considered, and ultimately why I chose Hugo as my platform for self-expression.

### Pros and Cons of Hugo

#### Pros:

1. **Speed and Performance:**
   - Hugo is renowned for its blazing-fast build times. It's built with Go, a statically typed, compiled language, which translates into remarkable speed when generating your website. This means quicker updates and reduced wait times.

2. **Flexibility and Customization:**
   - Hugo provides a high degree of flexibility in terms of theme selection and customization. With a wide variety of themes available, one can easily find one that aligns with their vision and branding. Customizing themes and layouts is also straightforward, thanks to Hugo's modular structure.

3. **Large and Active Community:**
   - The Hugo community is vibrant and welcoming. One will find extensive documentation, forums, and a wealth of online resources to help one troubleshoot issues and enhance their blog. The active development community ensures that Hugo stays up to date with the latest web technologies.

#### Cons:

1. **Steep Learning Curve:**
   - Hugo's speed and efficiency come at the cost of complexity. For beginners, the learning curve can be steep, especially if they're new to Markdown, Git, and the command line interface.

2. **Less Built-in Features:**
   - Compared to some other static site generators, Hugo offers fewer built-in features and plugins. While this can be an advantage for simplicity, it may require additional work if you want to add complex functionality to your blog.

### The Decision: Why Hugo?

After carefully weighing the pros and cons, I decided to go with Hugo for several reasons:

1. **Speed Matters:** Hugo's exceptional speed was a game-changer for me. I wanted the ability to publish content quickly without waiting for the site to rebuild, and Hugo's near-instantaneous build times offered exactly that.

2. **Community Support:** The active Hugo community was reassuring. I knew that if I encountered any issues or needed help with customization, there was a supportive community to turn to.

3. **Customization Potential:** Hugo's flexibility and ease of theme customization aligned perfectly with my vision for a personalized blog. I wanted a blog that not only showcased my content but also reflected my unique style and personality.

### Setting Up Hugo: A Step-by-Step Guide

#### 1. Installing Go and Hugo Extended

Before diving into Hugo, I ensured I had the necessary prerequisites in place:

- **Install Go:** Hugo is built with Go, so you'll need to [install Go](https://golang.org/doc/install) if you haven't already.

- **Install Hugo Extended:** Hugo Extended is the version of Hugo that includes additional features like SCSS processing. You can [download it here](https://github.com/gohugoio/hugo/releases).

#### 2. Selecting a Theme

Choosing the right theme for your blog is crucial. Hugo offers a wide selection of themes, both in its official theme gallery and on platforms like GitHub. Spend some time exploring themes that resonate with your style and content. For my purposes I chose [Jimmy's Stack theme](https://github.com/CaiJimmy/hugo-theme-stack) as I liked it's design and it is exactly what I needed from my blog.

#### 3. Cloning and Customizing the Theme

Once I had found the perfect theme, I had clone its repository. Stack's README was more than sufficient to get me started with this. After cloning and setting up, I started customizing the theme by modifying templates, colors, fonts, and adding my own branding elements along with my own social links and avatar.

#### 4. Pushing to GitHub
After making the changes I needed, I pushed the site to GitHub. I had expected it to work out of the box just as one might expect with Jekyll but in case of Hugo it didn't go as expected. I had to make some changes which I have described in the next step.

#### Deploying on GitHub Pages
After going through Hugo's documentation for GitHub pages, I got to know that in order to deploy my site automatically with GitHub pages I need to setup actions and provide it with a custom YAML which was given in Hugo's documentation [here](https://gohugo.io/hosting-and-deployment/hosting-on-github/). After going through the given steps and mentioning the branch which I would be using for deployment, I was able to setup an automatic routine for deployment. Now, each time I make a push to this repo, it will be automatically built and deployed. :grin:

## Conclusion
With these steps, I was well on my way to creating a personal blog that would be a canvas for my thoughts, experiences, and creative expressions. My journey to create a personal blog with Hugo and GitHub Pages was a fulfilling experience. It allowed me to exercise my creativity, establish a digital presence, and embrace the freedom of self-expression. The decision to choose Hugo, with its speed, flexibility, and vibrant community, felt like the right one for my journey of self-expression and creativity. As I embark on this blogging adventure, I look forward to sharing my thoughts, insights, and experiences with the world while maintaining complete control over my digital space. This "Hello World" blog is just the beginning of an exciting journey in the blogosphere and a starting point for maintaining my jorunal about LLM and Generative AI research. Cheers :v:

> Photo by [Pawel Czerwinski](https://unsplash.com/@pawel_czerwinski) on [Unsplash](https://unsplash.com/)