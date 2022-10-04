# Ticketeer - IN DEVELOPMENT

This software is meant to be used as a free ticketing-system that may be used by small organisations.

Currently this software is in development, which means that it is not expected to work in it's full functionality. I will keep a list of features that are planned and keep track if (I think) they are done.

## About

My personal incentive to develop this software is mostly to get used to Flask and proper software development of big flask applications. While the application consists of both backend and frontend, the software development focus for me will (for now) lie mostly in the backend part.

In my case the software will be used by local club I'm part of to track equipment-repairs. This way people can have a quick overview of what needs repairs and also who is responsible for such repairs.

## Planned Features

### Backend

- User-Management
  - Login (Receive JWT-Token)
  - Register new user
  - Fetching user data (search for single & multiple users)
  - Deleting users
  - Roles (via JWT-Tokens)
  - User-Icon mangement
- Ticket-Management
  - Create new tickets
  - Fetching ticket data (search for single & multiple tickets)
  - Deleting tickets
  - Assigning tickets to users
  - Adding tags to tickets
  - Changing ticket states

### Frontend

- Provide proper UI for backend features
