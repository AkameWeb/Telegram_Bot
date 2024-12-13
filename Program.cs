
using System;
using System.IO;
using System.Text;
using System.Threading;
using System.Threading.Tasks;
using Telegram.Bot;
using Telegram.Bot.Polling;
using Telegram.Bot.Types;
using Python.Runtime;
using System.Diagnostics;



namespace Telegram
{
    internal class Program
    {

        static ITelegramBotClient bot = new TelegramBotClient("7435745463:AAGdcvHPMFBPePos387QJO7fSMFfZvVXI7M");
        static void Main(string[] args)
        {
            ColorName();    
            User();
            
            Console.WriteLine("Запущен бот "+bot.GetMeAsync().Result);

            

           
            var cts = new CancellationTokenSource();
            var CT = cts.Token;
            var receiverOp = new ReceiverOptions()
            {
                AllowedUpdates = { },
            };
            bot.StartReceiving(HUAs,HErrorAs,receiverOp,CT);
            Console.ReadLine();
        }

        
        static async Task User()
        {
            
            Console.WriteLine(bot.GetMeAsync().Result.Username);
        }
        static async Task ColorName()
        {
            
            Console.WriteLine(bot.GetMeAsync().Result.FirstName);
        }
        public static void Dev()
        {
            Process.Start("python", "C:\\Users\\AkiWeb\\Desktop\\Telegram\\Telegram\\bin\\Debug\\Bot\\Bot\\bot.py");
        }

        public static async Task HUAs(ITelegramBotClient botClient, Update update, CancellationToken cancellationToken)
        {
            await Console.Out.WriteLineAsync(Newtonsoft.Json.JsonConvert.SerializeObject(update));
            if (update.Type == Telegram.Bot.Types.Enums.UpdateType.Message)
            {
                var message = update.Message;
                if (message.Text != null)
                {
                    Random numTEXT = new Random();
                    if (message.Text.ToLower() == "/start")
                    {
                        using (StreamWriter sw = new StreamWriter(Environment.CurrentDirectory + @"\Console" + numTEXT.Next() + ".txt", false, Encoding.Default))
                        {
                            Console.ForegroundColor = ConsoleColor.Green;
                            await Console.Out.WriteLineAsync($"{message.Chat.FirstName} | {message.Text} | {message.Chat.Location} | {message.Chat.Photo}");
                            sw.WriteLine($" ID = {message.Chat.Id} | UserName = {message.Chat.Username} | Name = {message.Chat.FirstName} | Text = {message.Text} | Location = {message.Chat.Location} | Photo = {message.Chat.Photo}");
                            
                            
                            await botClient.SendTextMessageAsync(message.Chat.Id, "Я безобидный бот)");
                            
                        }
                        return;
                    }


                    if (message.Text.ToLower() == "/stop")
                    {

                        await bot.DeleteMessageAsync(chatId: message.Chat.Id, messageId: message.MessageId, cancellationToken: cancellationToken);
                        Dev();
                        Environment.Exit(0);

                    }


                    using (StreamWriter sw = new StreamWriter(Environment.CurrentDirectory + @"\Console" + numTEXT.Next() + ".txt", false, Encoding.Default))
                    {
                        await Console.Out.WriteLineAsync($"{message.Chat.FirstName} | {message.Text} | {message.Chat.Location} | {message.Chat.Photo}");
                        sw.WriteLine($" ID = {message.Chat.Id} | UserName = {message.Chat.Username} | Name = {message.Chat.FirstName} | Text = {message.Text} | Location = {message.Chat.Location} | Photo = {message.Chat.Photo}");
                        Console.ForegroundColor = ConsoleColor.White;
                        //await botClient.SendTextMessageAsync(message.Chat.Id, message.Text);
                        
                    }
                    return;

            
                }
              
            }
        }

        public static async Task HErrorAs(ITelegramBotClient botClient, Exception exception, CancellationToken cancellationToken)
        {
            await Console.Out.WriteLineAsync(Newtonsoft.Json.JsonConvert.SerializeObject(exception));
        }
    }
}
