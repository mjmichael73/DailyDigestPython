import dd_content
import datetime
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv
from os import getenv

load_dotenv()


class DailyDigestEmail:

    def __init__(self):
        self.content = {
            'quote': {'include': True, 'content': dd_content.get_random_quote()},
            'weather': {'include': True, 'content': dd_content.get_weather_forecast()},
            'wikipedia': {'include': True, 'content': dd_content.get_wikipedia_article()}
        }
        self.recipients_list = []
        self.sender_credentials = {
            "email": getenv('SMTP_USERNAME'),
            "password": getenv('SMTP_PASSWORD')
        }

    def send_email(self):
        msg = EmailMessage()
        msg["Subject"] = f"Daily Digest - {datetime.date.today().strftime('%d %b %Y')}"
        msg["From"] = self.sender_credentials["email"]
        msg["to"] = ", ".join(self.recipients_list)

        msg_body = self.format_message()
        msg.set_content(msg_body["text"])
        msg.add_alternative(msg_body["html"], subtype="html")

        with smtplib.SMTP(getenv('SMTP_HOST'), int(getenv('SMTP_PORT'))) as server:
            server.starttls()
            server.login(self.sender_credentials["email"], self.sender_credentials["password"])
            server.send_message(msg)

        """
        Generate email message body as Plaintext and HTML.
        """

    def format_message(self):
        text = f'*~*~*~*~* Daily Digest - {datetime.date.today().strftime("%d %b %Y")} *~*~*~*~*\n\n'

        # format random quote
        if self.content['quote']['include'] and self.content['quote']['content']:
            text += '*~*~* Quote of the Day *~*~*\n\n'
            text += f'"{self.content["quote"]["content"]["quote"]}" - {self.content["quote"]["content"]["author"]}\n\n'

        # format weather forecast
        if self.content['weather']['include'] and self.content['weather']['content']:
            text += f'*~*~* Forecast for {self.content["weather"]["content"]["city"]}, {self.content["weather"]["content"]["country"]} *~*~*\n\n'
            for forecast in self.content['weather']['content']['periods']:
                text += f'{forecast["timestamp"].strftime("%d %b %H%M")} - {forecast["temp"]}\u00B0C | {forecast["description"]}\n'
            text += '\n'

        # format Wikipedia article
        if self.content['wikipedia']['include'] and self.content['wikipedia']['content']:
            text += '*~*~* Daily Random Learning *~*~*\n\n'
            text += f'{self.content["wikipedia"]["content"]["title"]}\n{self.content["wikipedia"]["content"]["extract"]}'

        #########################
        ##### Generate HTML #####
        #########################
        html = f"""<html>
    <body>
    <center>
        <h1>Daily Digest - {datetime.date.today().strftime('%d %b %Y')}</h1>
        """

        # format random quote
        if self.content['quote']['include'] and self.content['quote']['content']:
            html += f"""
        <h2>Quote of the Day</h2>
        <i>"{self.content['quote']['content']['quote']}"</i> - {self.content['quote']['content']['author']}
        """

        # format weather forecast
        if self.content['weather']['include'] and self.content['weather']['content']:
            html += f"""
        <h2>Forecast for {self.content['weather']['content']['city']}, {self.content['weather']['content']['country']}</h2> 
        <table>
                    """

            for forecast in self.content['weather']['content']['periods']:
                html += f"""
            <tr>
                <td>
                    {forecast['timestamp'].strftime('%d %b %H%M')}
                </td>
                <td>
                    <img src="{forecast['icon']}">
                </td>
                <td>
                    {forecast['temp']}\u00B0C | {forecast['description']}
                </td>
            </tr>
                        """

            html += """
            </table>
                    """
        # format Wikipedia article
        if self.content['wikipedia']['include'] and self.content['wikipedia']['content']:
            html += f"""
        <h2>Daily Random Learning</h2>
        <h3><a href="{self.content['wikipedia']['content']['url']}">{self.content['wikipedia']['content']['title']}</a></h3>
        <table width="800">
            <tr>
                <td>{self.content['wikipedia']['content']['extract']}</td>
            </tr>
        </table>
                    """

        # footer
        html += """
    </center>
    </body>
</html>
                """

        return {'text': text, 'html': html}


if __name__ == "__main__":
    email = DailyDigestEmail()
    email.send_email()
