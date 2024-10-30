# RaspberryPi News Notification Server

![Logo](./rpins_full_logo.webp)

![image](https://img.shields.io/badge/ChatGPT-74aa9c?style=for-the-badge&logo=openai&logoColor=white)
![image](https://img.shields.io/badge/Python-FFD43B?style=for-the-badge&logo=python&logoColor=blue)
![image](https://img.shields.io/badge/Docker-2CA5E0?style=for-the-badge&logo=docker&logoColor=white)
![License](https://img.shields.io/badge/license-MIT-blue)

If you want to know about the latest news from RaspberryPi this project might be for you!!

This Docker container continuously monitors the RSS feed of the RaspberryPi Newsfeed, meticulously analyzing any changes as they occur. By leveraging the capabilities of ChatGPT, it provides you with instant news notifications, ensuring you stay informed with the content that matters most to you. Whether it's new hardware, important announcements, or ryour favorite show, this system prioritizes the information you care about, delivering it directly to you in a concise and user-friendly format.

## Installation

The installation process is straightforward. Begin by creating the `config.yaml` file using the provided template. In this file, you'll need to specify three essential fields:

- **NTFY-Topic**: This field configures the notifications sent to your phone via the ntfy service. [Learn more about NTFY here](https://ntfy.sh)
- **OpenAI API Key**: This key is necessary for generating summaries and enabling decision-making.
- **Topic Priorities**: Specify your preferred topics for updates, such as new product launches. You can provide guidance to the AI about the topics you want to follow.


### Build Container:

Simply enter the following command into your terminal shell to build the docker image

```shell
sudo docker build -t rpi_newsroom_server .
```

### Run Container:

After that run the container using this command and you are good to go

```shell
sudo docker run -d --restart=unless-stopped --name=rpi_newsroom_notification_server rpi_newsroom_server 
```

## ChatGPT Integration

Please note that the decision to send a notification is made by ChatGPT. While it typically makes accurate decisions, there may be instances where notifications are sent more frequently than desired, or topics may be highlighted that were not specifically targeted. However, in my experience using the server, I have never received an incorrect notification, and ChatGPT does an excellent job of summarizing the news!

## Additional

In the `main.py` code, you'll find several adjustable settings that you can modify. While this script is tailored specifically for monitoring the RaspberryPi Newsroom RSS feed, it can easily be adapted to read a variety of other RSS feeds. I focused on this particular feed for simplicity and to cater to a community of fellow RaspberryPi News enthusiasts like myself :)

> And yes this Repository has a Twin [The Apple Newsroom Notification Server](https://github.com/pschuelpen/apple-news-notification-server) to keep you updated with the latest Apple Products

I hope you have fun with this !