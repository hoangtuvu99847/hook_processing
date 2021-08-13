

# if __name__ == '__main__':
#     s = Send()
#     try:
#         s.save_information()
#     except KeyboardInterrupt:
#         print('Interrupted')
#         s.payload = {'server': s.ip}
#         data = json.dumps(s.payload).encode('utf-8')
#         s.client.publish('disconnect_server', data)
#         sleep(3)
#         try:
#             sys.exit(0)
#         except SystemExit:
#             os._exit(0)


from collection.producer import RAMPublisher


if __name__ == '__main__':
    RAMPublisher().produce()
