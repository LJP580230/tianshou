import tensorflow as tf


def ppo_clip(policy, clip_param):
    """
    the clip loss in ppo paper

    :param sampled_action: placeholder of sampled actions during interaction with the environment
    :param advantage: placeholder of estimated advantage values.
    :param clip param: float or Tensor of type float.
    :param policy: current `policy` to be optimized
    :param pi_old: old `policy` for computing the ppo loss as in Eqn. (7) in the paper
    """
    action_ph = tf.placeholder(policy.act_dtype, shape=(None,) + policy.action_shape, name='ppo_clip_loss/action_placeholder')
    advantage_ph = tf.placeholder(tf.float32, shape=(None,), name='ppo_clip_loss/advantage_placeholder')
    policy.managed_placeholders['action'] = action_ph
    policy.managed_placeholders['processed_reward'] = advantage_ph

    log_pi_act = policy.log_prob(action_ph)
    log_pi_old_act = policy.log_prob_old(action_ph)
    ratio = tf.exp(log_pi_act - log_pi_old_act)
    clipped_ratio = tf.clip_by_value(ratio, 1. - clip_param, 1. + clip_param)
    ppo_clip_loss = -tf.reduce_mean(tf.minimum(ratio * advantage_ph, clipped_ratio * advantage_ph))
    return ppo_clip_loss


def vanilla_policy_gradient(sampled_action, reward, pi, baseline="None"):
    """
    vanilla policy gradient

    :param sampled_action: placeholder of sampled actions during interaction with the environment
    :param reward: placeholder of reward the 'sampled_action' get
    :param pi: current `policy` to be optimized
    :param baseline: the baseline method used to reduce the variance, default is 'None'
    :return:
    """
    log_pi_act = pi.log_prob(sampled_action)
    vanilla_policy_gradient_loss = tf.reduce_mean(reward * log_pi_act)
    # TODO: Different baseline methods like REINFORCE, etc.
    return vanilla_policy_gradient_loss

def dqn_loss(sampled_action, sampled_target, policy):
    """
    deep q-network

    :param sampled_action: placeholder of sampled actions during the interaction with the environment
    :param sampled_target: estimated Q(s,a)
    :param policy: current `policy` to be optimized
    :return:
    """
    sampled_q = policy.q_net.value_tensor
    return tf.reduce_mean(tf.square(sampled_target - sampled_q))

def deterministic_policy_gradient(sampled_state, critic):
    """
    deterministic policy gradient:

    :param sampled_action: placeholder of sampled actions during the interaction with the environment
    :param critic: current `value` function
    :return:
    """
    return tf.reduce_mean(critic.get_value(sampled_state))