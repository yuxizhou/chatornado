__author__ = 'yuxizhou'

import ujson
import nsq
import util

logger = util.get_logger(__name__, 'push-consumer.log')


def process_pm(message):
    try:
        c = ujson.loads(message.body)

        if c['event'] == 2:
            # p2p message
            pass
        elif c['event'] == 3:
            # group message
            if '__to' in c:
                # need push
                pass
            else:
                # group msg
                pass
    except Exception, e:
        logger.error(e)
        logger.error("process_pm ujson.loads fail [{}]".format(message.body))
    finally:
        message.finish()


reader = nsq.Reader(message_handler=process_pm,
                    lookupd_http_addresses=util.config['nsqlookupd'],
                    topic='pm', channel='async', max_in_flight=250)


if __name__ == "__main__":
    pass
