# Project Build Notes - Version 2

## What Was Fixed

1. **User Privacy**
   - Normal users now only access their own prediction history.
   - Admin-wide prediction logs are separated into the admin workspace.
   - The normal user sidebar does not expose admin-only pages.

2. **Role-Based Interface**
   - Normal users see recommendation, history, notifications, help, chat, and profile pages.
   - Admin users see admin dashboard, user management, prediction logs, model comparison, notifications, help, chat, and profile pages.

3. **Admin Capabilities**
   - Admin can edit user details.
   - Admin can change user role.
   - Admin can reset user password.
   - Admin can delete users.
   - Admin can delete individual prediction logs.
   - Admin can clear all prediction history for a selected user.
   - Admin can send broadcast notifications to all users.

4. **Sidebar and UI Cleanup**
   - Removed the old version label from the sidebar.
   - Added emoji-based sidebar navigation.
   - Fixed unreadable white selectbox/logout styling.
   - Reworked agriculture theme using green, brown, cream, and gold colors.

5. **Backgrounds and Page Design**
   - Added generated agriculture-style background images under assets/backgrounds/.
   - Each major page uses a specific faded background image.
   - Added page descriptions, cards, hover effects, and fade animations.

6. **Login Page**
   - Redesigned into a more professional dashboard-style landing/login page.
   - Removed non-working Google/Facebook login buttons.

## Design Decision

The rebuild keeps the FYP academically manageable. Production OAuth and live email delivery are not required for the core viva demo. The secure token recovery system remains implemented at demo level.


## Version 3 quick fixes
- Removed visible demo account credentials from the login page.
- Replaced all page background images with the provided smart agriculture dashboard image.
- Reduced the light overlay opacity so the background image is clearly visible while keeping text and cards readable.
