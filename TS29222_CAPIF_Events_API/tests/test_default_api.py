# coding: utf-8

from fastapi.testclient import TestClient


from capif_events.models.event_subscription import EventSubscription  # noqa: F401
from capif_events.models.problem_details import ProblemDetails  # noqa: F401


def test_subscriber_id_subscriptions_post(client: TestClient):
    """Test case for subscriber_id_subscriptions_post

    
    """
    event_subscription = {"notification_destination":"notificationDestination","event_filters":[{"aef_ids":["aefIds","aefIds"],"api_invoker_ids":["apiInvokerIds","apiInvokerIds"],"api_ids":["apiIds","apiIds"]},{"aef_ids":["aefIds","aefIds"],"api_invoker_ids":["apiInvokerIds","apiInvokerIds"],"api_ids":["apiIds","apiIds"]}],"supported_features":"supportedFeatures","event_req":{"partition_criteria":[None,None],"grp_rep_time":5,"mon_dur":"2000-01-23T04:56:07.000+00:00","imm_rep":1,"max_report_nbr":0,"rep_period":6,"samp_ratio":15},"websock_notif_config":{"request_websocket_uri":1,"websocket_uri":"websocketUri"},"events":[None,None],"request_test_notification":1}

    headers = {
    }
    response = client.request(
        "POST",
        "/{subscriberId}/subscriptions".format(subscriberId='subscriber_id_example'),
        headers=headers,
        json=event_subscription,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200


def test_subscriber_id_subscriptions_subscription_id_delete(client: TestClient):
    """Test case for subscriber_id_subscriptions_subscription_id_delete

    
    """

    headers = {
    }
    response = client.request(
        "DELETE",
        "/{subscriberId}/subscriptions/{subscriptionId}".format(subscriberId='subscriber_id_example', subscriptionId='subscription_id_example'),
        headers=headers,
    )

    # uncomment below to assert the status code of the HTTP response
    #assert response.status_code == 200

